
"""
   number of cmds that run on rpi pico
"""
import time
from machine import UART, RTC
from system.shared.strings import strs
from radiolib import radioMsg, reportBuffer
from radiolib.radioMsg import msgTypes
from system.shared.rtunodes import rtunodes
from system.shared.rtunode import rtunode
from system.cpuCore1.cmdSetDatetime import cmdSetDatetime


class radioCmds(object):

   def __init__(self, uart: UART,  msg: radioMsg):
      self.uart = uart
      self.msg = msg

   def execute(self, **kwargs) -> [None, bytearray]:
      try:
         cmd, argbuff = self.msg.get_cmd()
         print([cmd, argbuff])
         if cmd == msgTypes.READ_NODE_REGS:
            nodes: rtunodes = None
            if strs.KW_NODES in kwargs:
               nodes: rtunodes = kwargs[strs.KW_NODES]
            # -- return --
            rb: reportBuffer = self.__get_node_registers(argbuff, nodes)
            return rb.to_bytearray()
         elif cmd == msgTypes.SET_DATETIME:
            self.__set_datetime(argbuff)
         else:
            print(f"bad cmd: {cmd}")
         # -- return --
         return None
      except Exception as e:
         print(f"exec excep: {e}")

   def __get_node_registers(self, args, nodes: rtunodes) -> reportBuffer:
      args: str = args.decode(strs.UTF8)
      node: rtunode = nodes.get_node(args)
      rptbuff: reportBuffer = reportBuffer.reportBuffer()
      if node is None:
         rptbuff.extend(bytearray(f"{args}#ModbusNodeNotFound".encode()))
         rptbuff.set_error(0x00)
      else:
         rptbuff.extend(node.report())
         rptbuff.set_error(0x00)
      return rptbuff

   def __set_datetime(self, args):
      try:
         # b'20220116T003326UTC'
         print(f"__set_datetime: {args}")
         cmd: cmdSetDatetime = cmdSetDatetime(args)
         cmd.do()
         print(f"\t-- datetime set\n\t{time.localtime()}")
      except Exception as e:
         print(f"__set_datetime: {e}")

   def __add_node_model(self, args):
      pass

   def __add_model_register(self, args):
      pass

   def __add_node(self, args):
      pass


"""
   number of cmds that run on rpi pico
"""

from machine import UART
from system.shared.strings import strs
from radiolib import radioMsg
from radiolib.radioMsg import msgTypes
from system.shared.rtunodes import rtunodes
from system.shared.rtunode import rtunode


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
            return self.__get_node_registers(argbuff, nodes)
         elif cmd == msgTypes.SET_DATETIME:
            self.__set_datetime(argbuff)
         else:
            print(f"bad cmd: {cmd}")
         # -- return --
         return None
      except Exception as e:
         print(f"execute exception: {e}")

   def __get_node_registers(self, args, nodes: rtunodes) -> bytearray:
      args: str = args.decode("utf-8")
      print(f"__get_node_registers: {args}")
      node: rtunode = nodes.get_node(args)
      return node.report()

   def __set_datetime(self, args):
      # 2022 01 22 T 09 22 44
      print(f"__set_datetime: {args}")
      d, t = args.split("T")
      """y, mo, dd = d[:4], d[4:6], d[6:8]
      h, mn, s = d[:2], d[2:4], d[4:6]
      rtc: RTC = RTC((y, mo, dd, h, mn, s))
      print(rtc.datetime())"""

   def __add_node_model(self, args):
      pass

   def __add_model_register(self, args):
      pass

   def __add_node(self, args):
      pass

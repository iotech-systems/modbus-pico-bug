
import time, uasyncio
from system.config import CONFIG
from system.shared import __GBL__
from system.modbus.rturail import rturail
from system.shared.rtunode import rtunode
from system.shared.rtunodes import rtunodes
from system.modbus.memblock import memblock
from system.modbus.modbus import modbusConverter, Endian


NODES = None
KeyNodes = "nodes"
NODE_DELAY_MS = 100


async def modbusBot(**kwargs):
   print("-- modbusBot head --")
   # -- rtu nodes --
   global NODES
   if KeyNodes in kwargs:
      NODES = kwargs[KeyNodes]
   # -- rtu rail --
   rail: rturail = rturail(CONFIG)
   # -- loop --
   while True:
      try:
         __run__(rail, NODES)
         __GBL__.TASK_MODBUS_DTS = time.ticks_ms()
         await uasyncio.sleep_ms(CONFIG.MODBUS_BOT_DELAY_MS)
      except Exception as e:
         print(f"modbusBot: {e}")
   # -- end loop --


def __run__(rail: rturail, nodes: rtunodes) -> int:
   for node in nodes.arr:
      time.sleep_ms(NODE_DELAY_MS)
      node: rtunode = node
      if rail.ping(node):
         __sync_node__(rail, node)
      else:
         pass
   return 0


def __sync_node__(rail: rturail, node: rtunode):
   for reg in node.registers:
      reg: memblock = reg
      rail.sync_mem_block(node.modbus_id, reg)
      __update_memblock__(reg)
      reg.dump(_print=True)
   node.update_last_scanned()


def __update_memblock__(reg: memblock):
   mbc = modbusConverter(reg.rsp_memblock)
   if reg.ntype == memblock.FLOAT:
      reg.fltVal = mbc.decode_32bit_float(reg.dcpnt)
   elif reg.ntype == memblock.INT:
      reg.intVal = mbc.decode_32bit_int()
   else:
      pass

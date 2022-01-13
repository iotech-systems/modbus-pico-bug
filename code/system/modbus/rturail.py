
"""

"""

from system.config import config
from system.modbus import modbus
from system.modbus.memblock import memblock
from system.modbus.mb_pdu import mbPDU
from system.modbus.mb_adu import mbADU
from system.shared.rtunode import rtunode
from system.modbus.rtuwire import rtuwire
from system.shared.uartinfo import uartinfo


"""
   preps modbus packs to be loaded on the wire & sends them
   to rtuwire
"""


class rturail(object):

   def __init__(self, conf: config):
      self.conf = conf
      self.wire: rtuwire = rtuwire()

   def ping(self, node: rtunode) -> bool:
      uinfo: uartinfo = node.comm_info()
      self.wire.set_uartinfo(uinfo)
      rsp_adu = self.read_holding_registers(node.modbus_id
         , node.modbus_address_reg)
      if not self.__check_ping__(node, rsp_adu):
         print(f"Ping: {node.modbus_id} -> NoPong")
         return False
      # -- on true --
      print(f"Ping: {node.modbus_id} -> PongOK")
      return True

   def read_holding_registers(self, nodeID: int, reg: memblock) -> bytearray:
      """
         :param nodeID:
         :param reg:
         :return: response ADU
      """
      pdu = mbPDU.read_holding_registers(reg.address, reg.size)
      adu = mbADU.pack_pdu(nodeID, pdu)
      return self.wire.send_receive(adu, 48)

   def sync_mem_block(self, nodeID: int, reg: memblock):
      # print(f"\tsync_mem_block: @{nodeID} :: {reg.label}")
      reg.rsp_adu = self.read_holding_registers(nodeID, reg)
      reg.rsp_pdu = mbADU.unpack_pdu(reg.rsp_adu)
      reg.rsp_memblock = mbPDU.mem_block(reg.rsp_pdu)


   """
      protected 
   """
   def __check_ping__(self, node: rtunode, rsp_adu: bytearray) -> bool:
      try:
         if rsp_adu is None or len(rsp_adu) == 0:
            return False
         RCODE = mbADU.check_response(rsp_adu, node.modbus_id, modbus.READ_HOLDING_REGISTERS)
         if RCODE == 0:
            print("Good Response Buffer")
         elif RCODE == 1:
            print("Empty Response Buffer")
            return False
         elif RCODE == 2:
            print("Response Buffer with BAD CRC")
         elif RCODE == 4:
            pass
         elif RCODE == 8:
            pass
         else:
            pass
         # - - - - - -
         rsp_pdu = mbADU.unpack_pdu(rsp_adu)
         # print(f"rsp_pdu: {rsp_pdu}")
         mem_block = mbPDU.mem_block(rsp_pdu)
         val = modbus.utils.toShort(mem_block)
         # print(f"val: {val}")
         # - - - - - -
         return node.modbus_id == val
      except Exception as e:
         print(f"__check_ping__ err: {e}")
         return False

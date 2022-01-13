
import system.modbus.crc_utils as crc
from system.modbus.modbus import pduConsts, utils


class mbADU(object):

   @staticmethod
   def pack_pdu(nodeAdr, pdu) -> bytearray:
      serial_pdu = bytearray()
      serial_pdu.append(nodeAdr)
      serial_pdu.extend(pdu)
      crc16 = crc.calc_crc16(serial_pdu)
      serial_pdu.extend(crc16)
      return serial_pdu

   @staticmethod
   def check_response_address(expectedAdr: int, pdu) -> bool:
      respAdr = utils.toShort(pdu[1:])
      return expectedAdr == respAdr

   @staticmethod
   def check_response(res: bytearray, node_adr, function_code) -> int:
      RCODE = 0
      if len(res) == 0:
         # raise OSError("No Data Received from Node")
         return 1
      resp_crc = res[-crc.CRC_LENGTH:]
      expected_crc = crc.calc_crc16(res[0:len(res) - crc.CRC_LENGTH])
      if (resp_crc[0] != expected_crc[0]) or (resp_crc[1] != expected_crc[1]):
         # raise OSError("Invalid Response CRC")
         RCODE += 2
      if res[0] != node_adr:
         # raise ValueError("Wrong Node Address")
         RCODE += 4
      if res[1] == (function_code + pduConsts.ERROR_BIAS):
         # raise ValueError("Node Returned Exception Code: {:d}".format(res[2]))
         RCODE += 8
      # --- return ---
      return RCODE

   @staticmethod
   def unpack_pdu(adu: bytearray, count: int = 0):
      # print(f"\tunpack adu: {adu}")
      # -- 1 drops server address; -2 drops crc --
      pdu = adu[1:-2]
      # print(f"\t -> pdu: {pdu}")
      return pdu


"""hdr_length = (modbus.pduConsts.RESPONSE_HDR_LENGTH + 1) 
         if count else modbus.pduConsts.RESPONSE_HDR_LENGTH
   return respAdu[hdr_length:(len(respAdu) - crc.CRC_LENGTH)]"""

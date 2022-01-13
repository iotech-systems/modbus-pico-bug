
import struct


class byteutils(object):

   @staticmethod
   def to_short(buff: bytearray, signed: bool = True):
      rsp_quant = int(len(buff) / 2)
      fmt = '>' + (('h' if signed else 'H') * rsp_quant)
      tmp = struct.unpack(fmt, buff)
      return tmp[0]

   @staticmethod
   def node_id(barr: bytearray) -> int:
      tmp = struct.unpack(">B", barr)
      return int(tmp[0])

   def barr_to_byte(self, barr: bytearray) -> int:
      tmp = struct.unpack(">B", barr)
      return int(tmp[0])

   def int_to_bytes(self, id: chr) -> bytes:
      tmp = struct.pack(">B", id)
      return tmp

   def __msg_id_int__(self, barr: bytearray) -> int:
      tmp = struct.unpack(">I", barr)
      return int(tmp[0])

   def __msg_id_bytes__(self, id: int) -> bytes:
      tmp = struct.pack(">I", id)
      return tmp

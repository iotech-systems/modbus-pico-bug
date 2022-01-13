
import struct


READ_DISCRETE_INPUTS = 0x02

# -- coils --
READ_COILS = 0x01
WRITE_SINGLE_COIL = 0x05
WRITE_MULTIPLE_COILS = 0x0F

READ_INPUT_REGISTER = 0x04
READ_HOLDING_REGISTERS = 0x03
WRITE_SINGLE_REGISTER = 0x06
WRITE_MULTIPLE_REGISTERS = 0x10
READ_WRITE_MULTIPLE_REGISTERS = 0x17
MASK_WRITE_REGISTER = 0x16
READ_FIFO_QUEUE = 0x18

READ_FILE_RECORD = 0x14
WRITE_FILE_RECORD = 0x15

READ_EXCEPTION_STATUS = 0x07
DIAGNOSTICS = 0x08
GET_COM_EVENT_COUNTER = 0x0B
GET_COM_EVENT_LOG = 0x0C
REPORT_SERVER_ID = 0x11
READ_DEVICE_IDENTIFICATION = 0x2B

ops = {"READ_DISCRETE_INPUTS": 0x02, "READ_COILS": 0x01, "WRITE_SINGLE_COIL": 0x05
   , "WRITE_MULTIPLE_COILS": 0x0F, "READ_INPUT_REGISTER": 0x04, "READ_HOLDING_REGISTERS": 0x03
   , "WRITE_SINGLE_REGISTER": 0x06, "WRITE_MULTIPLE_REGISTERS": 0x10, "READ_WRITE_MULTIPLE_REGISTERS": 0x17
   , "MASK_WRITE_REGISTER": 0x16, "READ_FIFO_QUEUE": 0x18, "READ_FILE_RECORD": 0x14, "WRITE_FILE_RECORD": 0x15
   , "READ_EXCEPTION_STATUS": 0x07, "DIAGNOSTICS": 0x08, "GET_COM_EVENT_COUNTER": 0x0B
   , "GET_COM_EVENT_LOG": 0x0C, "REPORT_SERVER_ID": 0x11, "READ_DEVICE_IDENTIFICATION": 0x2B}


opsTable = {"0x06": "WRITE_SINGLE_REGISTER",
   "0x03": "READ_HOLDING_REGISTERS"}


class pduConsts:

   CRC_LENGTH = 0x02
   ERROR_BIAS = 0x80
   RESPONSE_HDR_LENGTH = 0x02
   ERROR_RESP_LEN = 0x05
   FIXED_RESP_LEN = 0x08
   MBAP_HDR_LENGTH = 0x07


class utils(object):

   @staticmethod
   def toShort(buff: bytearray, signed: bool = True):
      rsp_quant = int(len(buff) / 2)
      fmt = '>' + (('h' if signed else 'H') * rsp_quant)
      tmp = struct.unpack(fmt, buff)
      return tmp[0]


"""
   decoder code
"""


WC = {"b": 1, "h": 2, "e": 2, "i": 4,
    "l": 4, "q": 8, "f": 4, "d": 8}


class Endian(object):

   Auto = "@"
   Big = ">"
   Little = "<"


class modbusConverter(object):

   def __init__(self, regs: bytearray, byteorder=Endian.Little, wordorder=Endian.Big):
      self.payload: bytearray = regs
      self.byteorder = byteorder
      self.wordorder = wordorder
      self.pointer = 0x00

   def decode_32bit_float(self, rnd: int = 2) -> [False, float]:
      try:
         tmp = struct.unpack(">f", self.payload)[0]
         return round(tmp, rnd)
      except TypeError as e:
         print(f"decode_32bit_float: {e}")
         return False

   def decode_32bit_int(self) -> [False, int]:
      try:
         tmp = struct.unpack(">H", self.payload)[0]
         return tmp
      except TypeError as e:
         print(f"decode_32bit_int: {e}")
         return False

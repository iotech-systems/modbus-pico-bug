
"""
   https://www.ni.com/pl-pl/innovations/white-papers/14/the-modbus-protocol-in-depth.html
   The Modbus PDU:
      The PDU consists of a one-byte function code followed by up to 252 bytes of function-specific data.
"""

import struct
from system.modbus.mb_core import MB_FUNCTIONS


class pduConsts:

   CRC_LENGTH = 0x02
   ERROR_BIAS = 0x80
   RESPONSE_HDR_LENGTH = 0x02
   ERROR_RESP_LEN = 0x05
   FIXED_RESP_LEN = 0x08
   MBAP_HDR_LENGTH = 0x07


class mbPDU(object):

   @staticmethod
   def mem_block(barr: bytearray):
      # print(f"mem_block: {barr}")
      return barr[2:]

   @staticmethod
   def read_coils(start_reg, quantity):
      if not (1 <= quantity <= 2000):
         raise ValueError('invalid number of coils')
      return struct.pack('>BHH', MB_FUNCTIONS.READ_COILS
         , start_reg, quantity)

   @staticmethod
   def read_discrete_inputs(start_reg, quantity):
      if not (1 <= quantity <= 2000):
         raise ValueError('invalid number of discrete inputs')
      return struct.pack('>BHH', MB_FUNCTIONS.READ_DISCRETE_INPUTS
         , start_reg, quantity)

   @staticmethod
   def read_holding_registers(start_reg, quantity):
      if not (1 <= quantity <= 125):
         raise ValueError('invalid number of holding registers')
      return struct.pack('>BHH', MB_FUNCTIONS.READ_HOLDING_REGISTERS
         , start_reg, quantity)

   @staticmethod
   def read_input_registers(start_reg, quantity):
      if not (1 <= quantity <= 125):
         raise ValueError('invalid number of input registers')
      return struct.pack('>BHH', MB_FUNCTIONS.READ_INPUT_REGISTER
         , start_reg, quantity)

   @staticmethod
   def write_single_coil(output_address, output_value):
      if output_value not in [0x0000, 0xFF00]:
         raise ValueError('Illegal coil value')
      return struct.pack('>BHH', MB_FUNCTIONS.WRITE_SINGLE_COIL
         , output_address, output_value)

   @staticmethod
   def write_single_register(register_address, register_value, signed=True):
      fmt = 'h' if signed else 'H'
      return struct.pack('>BH' + fmt, MB_FUNCTIONS.WRITE_SINGLE_REGISTER
         , register_address, register_value)

   @staticmethod
   def write_multiple_coils(start_reg, value_list):
      sectioned_list = [value_list[i:i + 8] for i in range(0, len(value_list), 8)]
      output_value = []
      for index, byte in enumerate(sectioned_list):
         output = sum(v << i for i, v in enumerate(byte))
         output_value.append(output)
      fmt = 'B' * len(output_value)
      return struct.pack('>BHHB' + fmt, MB_FUNCTIONS.WRITE_MULTIPLE_COILS
         , start_reg, len(value_list), (len(value_list) // 8) + 1, *output_value)

   @staticmethod
   def write_multiple_registers(start_reg, register_values, signed=True):
      quantity = len(register_values)
      if not (1 <= quantity <= 123):
         raise ValueError('invalid number of registers')
      fmt = ('h' if signed else 'H') * quantity
      return struct.pack('>BHHB' + fmt, MB_FUNCTIONS.WRITE_MULTIPLE_REGISTERS
         , start_reg, quantity, quantity * 2, *register_values)

   @staticmethod
   def validate_resp_data(data, function_code, address, value=None, quantity=None, signed=True):
      if function_code in [MB_FUNCTIONS.WRITE_SINGLE_COIL, MB_FUNCTIONS.WRITE_SINGLE_REGISTER]:
         fmt = '>H' + ('h' if signed else 'H')
         resp_addr, resp_value = struct.unpack(fmt, data)
         if (address == resp_addr) and (value == resp_value):
            return True
      elif function_code in [MB_FUNCTIONS.WRITE_MULTIPLE_COILS, MB_FUNCTIONS.WRITE_MULTIPLE_REGISTERS]:
         resp_addr, resp_qty = struct.unpack('>HH', data)
         if (address == resp_addr) and (quantity == resp_qty):
            return True
      # -- return --
      return False

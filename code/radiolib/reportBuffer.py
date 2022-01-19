

class reportBuffer(object):

   ERROR_CODE_TMPL = "#%04d#"

   def __init__(self):
      self.err: bytearray = bytearray()
      self.barr: bytearray = bytearray()
      self.buff_sz: int = 0

   def __repr__(self):
      return f"err: {self.err}\nbarr: {self.barr}\nbuff_sz: {self.buff_sz}"

   def set_error(self, code: int):
      error = reportBuffer.ERROR_CODE_TMPL % code
      self.err = bytearray(error.encode())

   def extend(self, arr: bytearray):
      self.barr.extend(arr)

   def to_bytearray(self) -> bytearray:
      barr: bytearray = bytearray()
      barr.extend(self.err)
      barr.extend(self.barr)
      return barr

   def parse_bytes(self, arr: bytearray):
      self.buff_sz: int = arr[0]
      self.err = arr[2:8]
      self.barr = arr[8:]

   def report_size(self):
      return self.buff_sz

   @property
   def error_code(self) -> int:
      return int(self.err.decode().replace("#", "", 2))

   @property
   def error_msg(self) -> str:
      b = self.barr[4:].decode()
      return b

   @property
   def modbus_node_atid(self) -> str:
      return self.barr[0:4].decode()

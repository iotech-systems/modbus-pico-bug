

class reportBuffer(object):

   def __init__(self):
      self.err: bytearray = bytearray()
      self.barr: bytearray = bytearray()
      # --
      self.buff_sz: int = 0

   def set_error(self, code: int):
      error = "#%04d#" % code
      self.err = bytearray(error.encode())

   def extend(self, arr: bytearray):
      self.barr.extend(arr)

   def to_bytearray(self) -> bytearray:
      barr: bytearray = bytearray()
      barr.extend(self.err)
      barr.extend(self.barr)
      return barr

   def load_from_bytes(self, arr: bytearray):
      self.buff_sz: int = arr[0]
      self.err = arr[:6]
      self.barr = arr[6:]

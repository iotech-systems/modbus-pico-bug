

class reportBuffer(object):

   def __init__(self):
      self.err: bytearray = bytearray()
      self.barr: bytearray = bytearray()

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

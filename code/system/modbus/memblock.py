

class memblock(object):

   """
      0x0014:2:flt:2:GridFreqHz
   """

   FLOAT = "flt"
   INT = "int"

   def __init__(self, buff: str):
      hexbase = 16
      self.buff = buff
      if ":=" in self.buff:
         val = self.buff.split(":=")[1].strip()
      else:
         val = self.buff
      # -- --
      arr = val.split(":")
      if len(arr) != 5:
         raise ValueError(f"BadInput: {val}")
      # -- load --
      self.adrstr = arr[0]
      self.address = int(self.adrstr, hexbase)
      self.size = int(arr[1], 10)
      self.ntype = arr[2]
      self.dcpnt: int = int(arr[3])
      self.label = arr[4]
      # -- response stuff --
      self.rsp_adu: bytearray = None
      self.rsp_pdu: bytearray = None
      self.rsp_memblock: bytearray = None
      self.intVal: [False, int] = 0
      self.fltVal: [False, float] = 0.0

   def __repr__(self):
      return f"buff: {self.buff}"

   def set_adu_pdu(self, adu: bytearray, pdu: bytearray):
      self.rsp_adu = adu
      self.rsp_pdu = pdu

   def print_rsps(self):
      print([self.rsp_adu, self.rsp_pdu, self.rsp_memblock])

   def report(self) -> bytearray:
      rep: bytearray = bytearray()
      rep.extend(self.adrstr.encode())
      rep.extend(":".encode())
      rep.extend(self.rsp_memblock)
      return rep

   def dump(self, _print=False):
      buff = f"\t[label: {self.label} - address: {self.address} - intVal: {self.intVal} - fltVal: {self.fltVal}]"
      if _print:
         print(buff)
      else:
         return buff

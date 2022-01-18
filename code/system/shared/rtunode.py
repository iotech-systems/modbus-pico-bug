
import sys, time
from system.shared import uartinfo
from system.modbus.memblock import memblock
from radiolib.radioUtils import radioUtils


class rtunode(object):

   RS: chr = 0x1e

   def __init__(self, devString: str, conf):
      self.devString = devString
      self.conf = conf
      self.modbus_node_address: str = ""
      self.model_path = None
      # -- rtu info --
      self.modbus_address_reg: memblock = None
      self.comm = None
      self.registers = []
      self.last_scanned = None

   def __repr__(self):
      return f"- - -\n\t{self.comm}\n\t{self.modbus_address_reg}\n\t{self.registers}\n"

   def init(self):
      arr = self.devString.split("::")
      tmp: str = arr[0].strip()
      self.modbus_node_address = tmp[1:] if (tmp[0] == "@") else tmp
      self.model_path = arr[1].strip()
      if not self.__load_model_file__():
         print("unable to load model file")

   @property
   def modbus_id(self) -> int:
      if self.modbus_node_address is None:
         raise ValueError
      return int(self.modbus_node_address)

   def comm_info(self) -> uartinfo.uartinfo:
      return uartinfo.uartinfo(self.comm)

   def update_last_scanned(self):
      y, mo, d, h, mn, s, _, _ = time.localtime()
      self.last_scanned = (f"%s%02d%02dT%02d%02d%02d" % (y, mo, d, h, mn, s))

   def report(self) -> bytearray:
      rep: bytearray = bytearray()
      # -- set modbus node id to 3 chars --
      _srid = radioUtils.modbus_node_to_atid(self.modbus_id)
      rep.extend(_srid.encode())
      rep.extend(f"@{self.last_scanned}".encode())
      # -- for each memblock --
      for mb in self.registers:
         mb: memblock = mb
         rep.append(rtunode.RS)
         rep.extend(mb.report())
      # -- return --
      return rep

   def __load_model_file__(self) -> bool:
      try:
         filepath = self.model_path
         if sys.platform == "linux":
            filepath = self.model_path[1:]
         f = open(filepath, "r")
         for ln in f.readlines():
            ln = ln.strip()
            if ln.startswith("COMM:"):
               self.comm = ln.strip()
            if ln.startswith("ADDRESS_REG:"):
               self.modbus_address_reg = memblock(ln)
            if ln.startswith("0x"):
               reg = memblock(ln)
               self.registers.append(reg)
         f.close()
         return True
      except Exception as e:
         print(f"file not found: {e}")
         return False

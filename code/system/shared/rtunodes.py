
from system.shared.strings import strs
from system.shared.rtunode import rtunode
from system.config import CONFIG


class rtunodes(object):

   def __init__(self):
      self.arr: [] = []

   def load(self):
      with open(CONFIG.RTU_NODES_FILE, "r") as f:
         for ln in f.readlines():
            if ln.startswith("#"):
               continue
            node = rtunode(ln.strip(), CONFIG)
            self.arr.append(node)
      # init rtu devices
      for node in self.arr:
         node: rtunode = node
         node.init()
         print(node.registers)

   def print(self):
      for node in self.arr:
         print(node)

   def get_node(self, nodeid: int) -> [None, rtunode]:
      for n in self.arr:
         n: rtunode = n
         if n.modbus_id == nodeid:
            return n
      return None

   @property
   def items(self):
      return self.arr

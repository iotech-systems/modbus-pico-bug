

class radioUtils(object):

   @staticmethod
   def modbus_node_to_atid(nodeid: int) -> str:
      if nodeid > 247:
         raise ValueError("NodeIDOverMax")
      return "@%03d" % nodeid

   @staticmethod
   def modbus_node_fr_atid(nodeid: str) -> int:
      tmp = nodeid.replace("@", "")
      return int(tmp)


import struct
from radiolib.radioMsgLib import radioMsgLib


class msgIDGen(object):

   ID = 0

   @staticmethod
   def get_id() -> int:
      msgIDGen.ID += 1
      return msgIDGen.ID


class msgTypes(object):

   READ_NODE_REGS: bytearray = "RNRS".encode()
   SET_DATETIME: bytearray = "STDT".encode()
   ADD_MODEL: bytearray = "ADMD".encode()
   ADD_NODE: bytearray = "ADND".encode()
   MSG_ACK: bytearray = "MACK".encode()


class msgFlds(object):

   HEAD = [0, 3]           # bell, bell, vt
   TO_ID = [2, 5]          # vt, \x00\x00 - \x address, vt
   FR_ID = [4, 7]          # vt, 1b address, vt
   MSG_ID = [6, 12]        # vt, 4b seq, vt
   MSG_TYPE = [11, 17]     # vt, 4b seq, vt
   PLD_SIZE = [16, 19]     # vt, 2b, vt
   MSG_BD = [18, -1]
   # from the tail
   TAIL = [-2, None]       # vt, eot


class radioMsg(object):

   # -- data msg --
   BELL: chr = 0x07
   VT: chr = 0x0b
   EOT: chr = 0x04
   ACK: chr = 0x06
   MSG_HEAD = bytearray([BELL, BELL, VT])
   MSG_TAIL = bytearray([VT, EOT])
   MSG_VT = bytearray([VT])
   MSG_EOT = bytearray([EOT])
   # -- ping msg --
   PING_HEAD = bytearray([BELL, BELL, BELL])
   PING_TAIL = bytearray([BELL, EOT])
   PING_MSG = bytearray()
   PING_MSG.extend(PING_HEAD)
   PING_MSG.extend(bytearray([0x00, BELL, 0x00]))
   PING_MSG.extend(PING_TAIL)
   PING_SZ = len(PING_MSG)
   # -- pong msg --
   PONG_HEAD = bytearray([ACK, ACK, ACK])
   PONG_TAIL = bytearray([ACK, EOT])
   PONG_MSG = bytearray()
   PONG_MSG.extend(PONG_HEAD)
   PONG_MSG.extend(bytearray([0x00, ACK, 0x00]))
   PONG_MSG.extend(PONG_TAIL)

   @staticmethod
   def new_master_msg(toid: int, frid: int, mtype: bytearray, body: bytearray = None):
      mid: int = msgIDGen.get_id()
      return radioMsg.new_msg(toid, frid, mid, mtype, body)

   @staticmethod
   def new_msg(toid: int, frid: int, msgid: int
         , mtype: bytearray, body: bytearray = None) -> bytearray:
      barr: bytearray = bytearray()
      # -- add msg head --
      barr.extend(radioMsg.MSG_HEAD)
      # -- add msg to address --
      tmp = struct.pack(">B", toid)
      barr.extend(tmp)
      barr.extend(radioMsg.MSG_VT)
      # -- add msg from address --
      tmp = struct.pack(">B", frid)
      barr.extend(tmp)
      barr.extend(radioMsg.MSG_VT)
      # -- add msg id --
      # mid = msgIDGen.get_id()
      tmp = struct.pack(">I", msgid)
      barr.extend(tmp)
      barr.extend(radioMsg.MSG_VT)
      # -- add msg type address --
      barr.extend(mtype)
      barr.extend(radioMsg.MSG_VT)
      if body is not None:
         size = len(body)
         tmp = struct.pack(">B", size)
         barr.extend(tmp)
         barr.extend(radioMsg.MSG_VT)
         barr.extend(body)
      else:
         tmp = struct.pack(">B", 0)
         barr.extend(tmp)
         barr.extend(radioMsg.MSG_VT)
      barr.extend(radioMsg.MSG_TAIL)
      return barr

   @staticmethod
   def error_event_msg(nodeID, errorCode: int):
      radioMsgLib.EV_MSG[3] = nodeID
      radioMsgLib.EV_MSG[5] = errorCode
      return radioMsgLib.EV_MSG

   @staticmethod
   def rnrs_response(nodeID, barr: bytearray):
      buff: bytearray = bytearray()
      buff.extend(radioMsg.MSG_HEAD)
      nid = struct.pack(">B", nodeID)[0]
      buff.append(nid)
      buff.extend(radioMsg.MSG_VT)
      buff.extend(barr)
      buff.extend(radioMsg.MSG_TAIL)
      return buff

   @staticmethod
   def ping_msg(toid: int, frid: int):
      _toid = struct.pack(">B", toid)[0]
      _frid = struct.pack(">B", frid)[0]
      radioMsg.PING_MSG[3] = _toid
      radioMsg.PING_MSG[5] = _frid
      return radioMsg.PING_MSG

   @staticmethod
   def is_ping(barr: bytearray):
      if len(barr) != radioMsg.PING_SZ:
         return False
      # -- could be ping --
      return radioMsg.PING_HEAD == barr[:3] and radioMsg.PING_TAIL == barr[-2:]

   @staticmethod
   def is_ping_for_this_node(barr: bytearray, nodeID: int):
      _nid: int = int(barr[3])
      return _nid == nodeID

   @staticmethod
   def pong_msg(barr: bytearray):
      _nid: chr = barr[3]
      _fid: chr = barr[5]
      radioMsg.PONG_MSG[3] = _fid
      radioMsg.PONG_MSG[5] = _nid
      return radioMsg.PONG_MSG

   @staticmethod
   def is_pong_good(pingTo: int, pingFr: int, pong: bytearray) -> bool:
      bh = (radioMsgLib.PONG_HEAD == pong[:3])
      be = (radioMsgLib.PONG_TAIL == pong[-2:])
      _nid: chr = pong[3]
      _fid: chr = pong[5]
      tofrom: bool = (pingTo == _fid) and (pingFr == _nid)
      return bh and be and tofrom

   @staticmethod
   def test_vts(buff: bytearray):
      vts = buff[:1]
      vte = buff[-1:]
      return vts == radioMsg.MSG_VT and vte == radioMsg.MSG_VT

   @staticmethod
   def is_good_ack(targetNodeID: int, msgID: int, ack: bytearray):
      nid = ack[5]
      mid: int = struct.unpack(">I", ack[7:11])[0]
      return targetNodeID == nid and msgID == mid

   def __init__(self, buff: bytearray):
      self.buff = buff
      self.to_id = 0
      self.fr_id = 0
      self.msg_id = 0
      self.msg_tp = None
      self.msg_bd: bytearray = None
      self.msg_sz = 0

   def is_valid_head_tail(self) -> bool:
      head = self.__sub_buff__(msgFlds.HEAD)
      tail = self.__sub_buff__(msgFlds.TAIL)
      return head == radioMsg.MSG_HEAD and tail == radioMsg.MSG_TAIL

   def is_for_this_node(self, nodeID: int):
      barr = self.__sub_buff__(msgFlds.TO_ID)
      if not self.__test_vts__(barr):
         raise ValueError("BAD_VTs")
      barr = self.__strip_vts__(barr)
      nid = struct.unpack(">B", barr)[0]
      return nid in (nodeID, 0xff)

   def unpack(self):
      try:
         # -- msg to --
         arr = self.__sub_buff__(msgFlds.TO_ID)
         arr = self.__strip_vts__(arr)
         self.to_id = struct.unpack(">B", arr)[0]
         # -- msg from --
         arr = self.__sub_buff__(msgFlds.FR_ID)
         arr = self.__strip_vts__(arr)
         self.fr_id = struct.unpack(">B", arr)[0]
         # -- msg id --
         arr = self.__sub_buff__(msgFlds.MSG_ID)
         arr = self.__strip_vts__(arr)
         self.msg_id = struct.unpack(">I", arr)[0]
         # -- msg type --
         arr = self.__sub_buff__(msgFlds.MSG_TYPE)
         arr = self.__strip_vts__(arr)
         self.msg_tp = struct.unpack("4s", arr)[0]
         # -- body size --
         arr = self.__sub_buff__(msgFlds.PLD_SIZE)
         arr = self.__strip_vts__(arr)
         self.msg_sz = struct.unpack(">B", arr)[0]
         # -- body --
         arr = self.__sub_buff__(msgFlds.MSG_BD)
         arr = self.__strip_vts__(arr)
         if not self.msg_sz == len(arr):
            return False
         fmt = f"{self.msg_sz}s"
         self.msg_bd = struct.unpack(fmt, arr)[0]
         return True
      except:
         return False

   def ack_msg(self) -> bytearray:
      barr: bytearray = bytearray()
      # -- add msg head --
      barr.extend(radioMsg.MSG_HEAD)
      # -- add msg to address --
      tmp = struct.pack(">B", self.fr_id)
      barr.extend(tmp)
      barr.extend(radioMsg.MSG_VT)
      # -- add msg from address --
      tmp = struct.pack(">B", self.to_id)
      barr.extend(tmp)
      barr.extend(radioMsg.MSG_VT)
      # -- add msg id --
      tmp = struct.pack(">I", self.msg_id)
      barr.extend(tmp)
      barr.extend(radioMsg.MSG_VT)
      # -- add msg type address --
      barr.extend(msgTypes.MSG_ACK)
      barr.extend(radioMsg.MSG_VT)
      # -- incoming msg payload size --
      tmp = struct.pack(">B", self.msg_sz)
      barr.extend(tmp)
      barr.extend(radioMsg.MSG_VT)
      barr.extend(radioMsg.MSG_TAIL)
      return barr

   def get_cmd(self) -> (bytearray, bytearray):
      return self.msg_tp, self.msg_bd

   def response_msg(self, barr: bytearray):
      arr = radioMsg.new_msg(self.fr_id, self.to_id, self.msg_id, self.msg_tp, barr)
      return arr

   def __test_vts__(self, buff: bytearray):
      vts = buff[:1]
      vte = buff[-1:]
      return vts == radioMsg.MSG_VT and vte == radioMsg.MSG_VT

   def __sub_buff__(self, idxs: []):
      if len(idxs) != 2:
         raise ValueError("")
      s, e = idxs
      return self.buff[s:e]

   def __strip_vts__(self, barr: bytearray) -> [None, bytearray]:
      if self.__test_vts__(barr):
         return barr[1:-1]
      else:
         return None

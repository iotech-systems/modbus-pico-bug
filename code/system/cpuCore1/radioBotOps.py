
import time
from machine import UART
from system.config import CONFIG
from system.shared.rtunode import rtunode
from system.shared.rtunodes import rtunodes
from system.modbus.memblock import memblock


class CMDS:

   READREGS = "READREGS"
   SETTIME = "SETTIME"
   FREFRESH = "FREFRESH"


NODE_HDR = "#!:".encode()
NODE_TAL = ":!#".encode()
SERV_HDR = "!#:".encode()
SERV_TAL = ":#!".encode()
ACK_MSG = "!#:0x00:{0}:ACK#!\n"

BELL: chr = 0x07
VT: chr = 0x0b
EOT: chr = 0x04
MSG_HEAD = bytearray([BELL, BELL, VT])
MSG_TAIL = bytearray([VT, EOT])


class radioBotOps(object):

   @staticmethod
   def check_msgin(MSGIN: bytearray) -> [False, []]:
      head, tail = MSGIN[0:3], MSGIN[-2:]
      if not (head == MSG_HEAD and tail == MSG_TAIL):
         return False
      args = MSGIN[3:-3].decode("utf-8").split(":")
      if int(args[0], 16) != CONFIG.radioID:
         print("\nmsg is not for this node\n")
         return False
      # -- msgin is this node --
      print("\nmsg is for this node\n")
      return args

   def __init__(self, uart: UART, nodes: rtunodes):
      self.uart = uart
      self.nodes = nodes

   def ack_msgin(self, buff: str):
      self.uart.read()
      m = ACK_MSG.format(hex(CONFIG.radioID))
      cnt = self.uart.write(bytearray(m))
      if cnt == len(buff):
         print("ack sent")

   def process_args(self, args: []):
      if args[1] == CMDS.READREGS:
         self.__readregs__(args)

   def __readregs__(self, args: []):
      nodeid = args[2]
      print(f"__readregs__: {nodeid}")
      node: rtunode = self.nodes.get_node(nodeid)
      for r in node.registers:
         r: memblock = r
         print(f"sending: {r.dump()}")
         barr = bytearray(f"{r.dump()}\n")
         self.uart.write(barr)

   def __send_msg__(self, msg: str):
      self.uart.write(bytearray(msg))

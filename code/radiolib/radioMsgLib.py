
class radioErrors(object):

   ERROR_OK = 0
   REPORT_ERROR = 1001


class errorEvents(object):

   UNPACK_ERROR = 13


class radioMsgLib(object):

   BELL: chr = 0x07
   VT: chr = 0x0b
   EOT: chr = 0x04
   ACK: chr = 0x06
   SYNC: chr = 0x16

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

   # -- error event --
   EV_HEAD = bytearray([SYNC, SYNC, SYNC])
   EV_TAIL = bytearray([SYNC, EOT])
   EV_MSG = bytearray()
   EV_MSG.extend(EV_HEAD)
   EV_MSG.extend(bytearray([0x00, ACK, 0x00]))
   EV_MSG.extend(EV_TAIL)

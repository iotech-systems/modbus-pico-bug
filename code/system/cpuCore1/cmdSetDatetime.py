
import time
from machine import RTC
from system.config import CONFIG
from system.shared.strings import strs


class cmdSetDatetime(object):

   def __init__(self, args: bytearray):
      self.args = args

   def do(self):
      d = self.args[:8]
      t = self.args[9:15]
      tz = self.args[-3:].decode(strs.UTF8).upper()
      if tz not in CONFIG.TZs:
         print(strs.BAD_TZ)
      CONFIG.SYS_TZ = tz
      y, mo, dd = int(d[:4].decode(strs.UTF8)), \
         int(d[4:6].decode(strs.UTF8)), int(d[6:8].decode(strs.UTF8))
      h, mn, sc = int(t[:2].decode(strs.UTF8)), \
         int(t[2:4].decode(strs.UTF8)), int(t[4:6].decode(strs.UTF8))
      dow = 0; subsec = 0
      tpl = (y, mo, dd, dow, h, mn, sc, subsec)
      rtc: RTC = RTC()
      rtc.datetime(tpl)


# -- tests --
if __name__ == "__main__":
   barr = bytearray(b'20220116T093326UTC')
   cmd: cmdSetDatetime = cmdSetDatetime(barr)
   cmd.do()

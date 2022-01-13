
"""
   COMM:= buad/8n1/timeout/char_timeout
   COMM:= 9600/8N1/20/8
"""

import sys


PARITIES = {"N": None, "E": 0, "0": 1}


class parityTable:

   @staticmethod
   def get_table():
      if sys.platform == "linux":
         return {"N": "N", "E": "E", "O": "O"}
      elif sys.platform == "rp2":
         return {"N": None, "E": 0, "O": 1}
      else:
         raise SystemError("BadSystemPlatform")


class uartinfo(object):

   def __init__(self, comminfo: str):
      token = "COMM:="
      if not comminfo.startswith(token):
         raise ValueError("BadCommString")
      self.comminfo = comminfo.replace(token, "").strip()
      arr = self.comminfo.split("/")
      self.__baud = int(arr[0].strip())
      cb, pa, sb = arr[1].strip()
      if pa not in PARITIES:
         raise ValueError("BadParity")
      self.__parity = pa
      self.__charbits = int(cb)
      self.__stopbits = int(sb)
      self.__timeout = int(arr[2])
      self.__timeout_char = int(arr[3])

   @property
   def baud(self) -> int:
      return self.__baud

   @property
   def parity(self) -> [None, int, chr]:
      if sys.platform == "rp2":
         return PARITIES[self.__parity]
      else:
         return self.__parity

   @property
   def charbits(self) -> int:
      return self.__charbits

   @property
   def stopbits(self) -> int:
      return self.__stopbits

   @property
   def timeout(self) -> int:
      return self.__timeout

   @property
   def timeout_char(self) -> int:
      return self.__timeout_char

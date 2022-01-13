#!/usr/bin/env python3

import os, serial, time, random
os.chdir("code")
print(os.getcwd())
from test_ping_pong import ping_pong

ser: serial.Serial
try:
   ser = serial.Serial(port="/dev/ttyUSB0", baudrate=2400)
except:
   pass


def main():
   while True:
      print("--main--")
      ping_pong(ser)
      v = random.randrange(8, 16)
      print(f"sleeping: {v}")
      time.sleep(v)


# -- main --
if __name__ == "__main__":
   main()

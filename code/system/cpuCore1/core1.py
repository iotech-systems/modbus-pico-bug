
"""
   parity is the parity, None, 0 (even) or 1 (odd).
"""

import time
from machine import Timer
from system.config import config
from system.shared.cpuCore import cpuCore
from system.modbus.rtuDevice import rtuDevice
from system.cpuCore1 import radioBot, modbusBot


__DEBUG__ = True
WIRE_UART_ID = 0
WIRE_SEND_PIN = 2
LORA_UART_ID = 1
BAUDRATE = 9600

INTERVAL_2MS = 2
INTERVAL_1MN = 60000
INTERVAL_6MN = 6 * INTERVAL_1MN
LORA_INTERVAL = INTERVAL_2MS
MODBUS_INTERVAL = INTERVAL_1MN

SYS_TIMER_PERIOD = 8000
CORE1_MON_TIMER: Timer
CONFIG = config()
parityMap = {"N": None, "E": 0, "O": 1}


class core1(cpuCore):

   def __init__(self):
      super().__init__()

   def run(self, args: ()):
      pass

   def run1(self, args: ()):
      loop_counter = 0
      while True:
         loop_counter += 1
         delay = 400 * loop_counter
         print(f"delay: {delay}")
         time.sleep_ms(delay)
         self.lastTicksMS = time.ticks_ms()

   def load_nodes(self):
      pass

   def __run__(self):
      pass

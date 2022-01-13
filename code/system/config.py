
import os, sys
from machine import Pin


print(f"\n[ platform: {sys.platform} ]\n")
LED_PIN_NUMER = 25


class config(object):

   def __init__(self):
      self.KILO = 1000
      self.KILOBYTE = 1024
      self.platform = sys.platform
      self.radioID: int = 161
      self.RSE_PIN = 2
      self.LED_PIN = Pin(LED_PIN_NUMER, Pin.OUT)
      self.RTU_NODES_FILE = "nodes/rtu.devices"
      self.modbusUARTID = 0
      self.__set_lora_id__()
      # COMM:= buad/8n1/timeout/char_timeout
      self.RADIO_COMM_INFO = "COMM:= 2400/8N1/40/6"
      self.RADIO_BOT_DELAY_MS = 4
      self.RADIO_UART_ID = 1
      self.MODBUS_BOT_DELAY_MS = 32000
      self.MODBUS_UART_ID = 0
      self.Baud9600 = 9600
      # -- monitor timers --
      self.CORE0_MON_TIMER: int = (self.KILO * 8)
      self.CORE1_MON_TIMER: int = (self.KILO * 8)
      # -- logs --
      self.RUNTIME_LOG_SIZE_KB = 200
      self.RUNTIME_LOG_FILE = "/logs/runtime.log"

   def __set_lora_id__(self):
      try:
         with open("/airbus.id", "r") as r:
            self.radioID = int(r.read().strip(), 16)
      except IOError:
         print("FileNotFound")


# -- create object --
CONFIG = config()

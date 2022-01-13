
import time
from system.config import CONFIG
from machine import Pin


def core0_monitor(t):
   print(f"--- core0_monitor: {t}")
   blink_led(CONFIG.LED_PIN, 8, 80)


def blink_led(led: Pin, cnt: int, delayMS: int):
   for i in range(0, cnt):
      time.sleep_ms(delayMS)
      led.toggle()
   # -- turn off --
   led.off()

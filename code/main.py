
"""
   proxy loop will run on core1
"""

import sys, time, _thread
from machine import Timer
from system.config import CONFIG
from system.cpuCore0.core0 import core0
from system.cpuCore1.core1init import core1Init
from system.cpuCore0.core0tasks import core0_monitor


START_DELAY = 2
# main code runs on core0 starts the system
CORE0: core0
CORE0_MONITOR_TIMER: Timer = Timer(period=CONFIG.CORE0_MON_TIMER
   , mode=Timer.PERIODIC, callback=core0_monitor)


def main():
   # -- start system 1: start this first as core0 start is not returning --
   print("\n[ main ]")
   _thread.start_new_thread(core1Init, ())
   # -- small delay --
   time.sleep_ms(START_DELAY)
   # -- let core0 start --
   global CORE0
   CORE0 = core0()
   CORE0.run(None)


# -- entry point --
if __name__ == "__main__":
   main()
# -- end --

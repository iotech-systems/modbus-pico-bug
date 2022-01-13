
import time, gc
from machine import Pin
from system.shared.cpuCore import cpuCore


class core0(cpuCore):

   def __init__(self):
      super().__init__()
      self.args: () = None
      self.led = Pin(25, Pin.OUT)

   def run(self, args: ()):
      self.args = args
      while True:
         if self.__run__():
            # self.__push_run_state__(self.led)
            time.sleep(16.0)
         else:
            pass

   def __run__(self) -> bool:
      print("core0.__run__")
      try:
         print(f"\n\t--- gc info ---\n\tfree: {gc.mem_free()}\n\talloc: {gc.mem_alloc()}\n\t--- end gc info ---")
         gc.collect()
         print(f"\n\t--- gc info ---\n\tfree: {gc.mem_free()}\n\talloc: {gc.mem_alloc()}\n\t--- end gc info ---")
      except Exception as e:
         print(e)
         return False
      finally:
         return True

   def __push_run_state__(self, led: Pin, tx: Pin = None):
      # -- flash pin --
      led.on()
      time.sleep(0.2)
      led.off()
      # TODO: send string to tx pin

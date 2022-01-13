
import uasyncio, gc
from machine import Timer
from system.shared import __GBL__
from system.config import CONFIG
from system.cpuCore1.radioBot import radioBot
from system.cpuCore1.modbusBot import modbusBot
from system.shared.rtunodes import rtunodes
from system.cpuCore1.core1tasks import core1_monitor
from system.shared.strings import strs


# parityMap = {"N": None, "E": 0, "O": 1}
CORE1_MONITOR_TIMER = Timer(period=CONFIG.CORE1_MON_TIMER
   , mode=Timer.PERIODIC, callback=core1_monitor)

RTU_NODES: rtunodes = rtunodes()
RTU_NODES.load()


def start_coroutines() -> bool:
   try:
      __GBL__.EVENT_LOOP = None
      __GBL__.EVENT_LOOP = uasyncio.get_event_loop()
      __GBL__.EVENT_LOOP.set_exception_handler(__loop_exception_handler__)
      loraTask: uasyncio.Task = __GBL__.EVENT_LOOP.create_task(radioBot(nodes=RTU_NODES))
      __GBL__.CORE1_TASKS.append(loraTask)
      modbusTask: uasyncio.Task = __GBL__.EVENT_LOOP.create_task(modbusBot(nodes=RTU_NODES))
      __GBL__.CORE1_TASKS.append(modbusTask)
      __GBL__.EVENT_LOOP.run_forever()
      return True
   except Exception as e:
      print(e)
      return False


def __loop_exception_handler__(loop, context):
   try:
      h = "__loop_exception_handler__"
      print(f"\n\t{h}\n")
      exp = context["exception"]
      print([loop, context, exp])
      loop.stop()
      loop.close()
   finally:
      gc.collect()


def core1Main():
   try:
      if start_coroutines():
         print("start_coroutines: ok")
      else:
         print("start_coroutines: error")
   except Exception as e:
      print(e)


def core1Init():
   try:
      core1Main()
   except Exception as e:
      print(e)



from system.shared import __GBL__


def core1_monitor(t):
   print(f"\n--- core1_monitor: {t}")
   print(f"\tmodbus dts: {__GBL__.TASK_MODBUS_DTS}")
   print(f"\tlora dts: {__GBL__.TASK_LORA_DTS}")

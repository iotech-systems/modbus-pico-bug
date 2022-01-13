
from machine import UART

TASK_MODBUS_DTS = 0
TASK_LORA_DTS = 0
CORE1_THREAD = None
EVENT_LOOP = None
CORE1_TASKS = []
__UART_MB__: UART = None
__UART_RD__: UART = None


import uasyncio, time, math
from machine import UART
from system.config import CONFIG
from system.shared import __GBL__
from radiolib.radioMsg import radioMsg
from radiolib.radioMsgLib import errorEvents
from system.cpuCore1.radioCmds import radioCmds
from system.shared.rtunode import rtunode
from system.shared.uartinfo import uartinfo
from system.shared.rtunodes import rtunodes
from system.modbus.memblock import memblock


KeyNodes = "nodes"
NODES: rtunodes = None
LOOP_COUNTER = 0
MIN_MSG_SIZE = 8
ticks = 0
MSGIN: bytearray = bytearray(64)
CHARACTER_DELAY = 0


async def radioBot(**kwargs):
   hd = "\n\t[ radio head ]"
   print(hd)
   global NODES, CHARACTER_DELAY
   if KeyNodes in kwargs:
      NODES: rtunodes = kwargs[KeyNodes]
   # -- setup radio uart --
   info: uartinfo = uartinfo(CONFIG.RADIO_COMM_INFO)
   CHARACTER_DELAY = math.ceil((1 / (info.baud / 11)) * CONFIG.KILO)
   print(f"CHARACTER_DELAY: {CHARACTER_DELAY}")
   __GBL__.__UART_RD__ = __uart__(info, CONFIG)
   run_count = 0
   old_ticks = time.ticks_ms()
   # -- loop --
   while True:
      try:
         run_count += 1
         msdiff = time.ticks_diff(time.ticks_ms(), old_ticks)
         if msdiff > 8000:
            print(f"\tticks: {msdiff} :: run_count: {run_count}")
            old_ticks = time.ticks_ms()
            run_count = 0
         # -- check radio uart; can hold max 64 chars; packets will be 8 or 48 chars --
         buff: bytearray = None
         if __GBL__.__UART_RD__.any():
            buff = __read_from_uart__(CHARACTER_DELAY)
         # -- process buffer --
         if buff is not None:
            __run__(buff)
         __GBL__.TASK_LORA_DTS = time.ticks_ms()
         await uasyncio.sleep_ms(CONFIG.RADIO_BOT_DELAY_MS)
      except Exception as e:
         print(f"\n\tradiobot exception: {e}\n")
   # -- end loop --


def __run__(msgin: bytearray) -> int:
   # -- run --
   print(f"\n\t[ MSGIN: {msgin} ]\n")
   # -- is ping is so do pong and return --
   if radioMsg.is_ping(msgin):
      if radioMsg.is_ping_for_this_node(msgin, CONFIG.radioID):
         pong = radioMsg.pong_msg(msgin)
         __send_barr__(pong)
         return 0
   # -- run --
   radio_msg: radioMsg = radioMsg(msgin)
   if not radio_msg.is_valid_head_tail():
      return 0
   if not radio_msg.is_for_this_node(CONFIG.radioID):
      return 0
   # -- msg is for this node --
   if not radio_msg.unpack():
      # -- broadcast error event as unable to unpack --
      barr = radioMsg.error_event_msg(CONFIG.radioID, errorEvents.UNPACK_ERROR)
      __send_str__(barr)
      return 0
   # -- send back ack msg --
   ack: bytearray = radio_msg.ack_msg()
   __send_barr__(ack)
   time.sleep_ms(CONFIG.POST_ACK_DELAY_MS)
   # -- will need to assume as time limits here --
   radio_cmds: radioCmds = radioCmds(__GBL__.__UART_RD__, radio_msg)
   rbuff = radio_cmds.execute(nodes=NODES)
   if rbuff is not None:
      arr = radio_msg.response_msg(rbuff)
      __send_barr__(arr)
   return 0


def __send_all_registers__():
   for node in NODES.items:
      node: rtunode = node
      print(f"\n\tnode: @{node.modbus_id}")
      for reg in node.registers:
         reg: memblock = reg
         __send_str__(reg.dump())


def __is_msg_in_tx_buffer__():
   pass


def __send_str__(buff: str):
   bs = bytearray(f"{buff}\n")
   cnt = __GBL__.__UART_RD__.write(bs)
   print(f"bytes sent: {cnt}")


def __send_barr__(barr: bytearray):
   cnt = __GBL__.__UART_RD__.write(barr)
   write_delay = (len(barr) * CHARACTER_DELAY)
   print(f"\tbytes sent: {cnt} | write_delay: {write_delay}")
   time.sleep_ms(write_delay)


"""      
"""
def __read_from_uart__(CHAR_DELAY) -> bytearray:
   buff: bytearray = bytearray()
   while __GBL__.__UART_RD__.any():
      buff.extend(__GBL__.__UART_RD__.read(1))
      # -- this seems to be needed here; need to research this bit more --
      time.sleep_ms(CHAR_DELAY)
   return buff


def __uart__(uinfo: uartinfo, conf):
   return UART(conf.RADIO_UART_ID
      , baudrate=uinfo.baud
      , parity=uinfo.parity
      , stop=uinfo.stopbits
      , bits=uinfo.charbits
      , timeout=uinfo.timeout
      , timeout_char=uinfo.timeout_char)

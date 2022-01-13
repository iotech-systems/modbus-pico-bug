
"""
   UART.init(baudrate=9600, bits=8, parity=None, stop=1, *, ...)
   Initialise the UART bus with the given parameters:
            baudrate is the clock rate.
            bits is the number of bits per character, 7, 8 or 9.
            parity is the parity, None, 0 (even) or 1 (odd).
            stop is the number of stop bits, 1 or 2.
   Additional keyword-only parameters that may be supported by a port are:
      tx specifies the TX pin to use.
      rx specifies the RX pin to use.
      rts specifies the RTS (output) pin to use for hardware receive flow control.
      cts specifies the CTS (input) pin to use for hardware transmit flow control.
      txbuf specifies the length in characters of the TX buffer.
      rxbuf specifies the length in characters of the RX buffer.
      timeout specifies the time to wait for the first character (in ms).
      timeout_char specifies the time to wait between characters (in ms).
      invert specifies which lines to invert.
      flow specifies which hardware flow control signals to use. The value is a bitmask.
              0 will ignore hardware flow control signals.
              UART.RTS will enable receive flow control by using the RTS output pin to signal if the receive
              FIFO has sufficient space to accept more data.
              UART.CTS will enable transmit flow control by pausing transmission when the CTS input pin
              signals that the receiver is running low on buffer space.
              UART.RTS | UART.CTS will enable both, for full hardware flow control.
"""


import time, uasyncio
from machine import UART, Timer
from system.shared import __GBL__
from system.config import CONFIG
from system.shared.uartinfo import uartinfo
from system.shared.exceptions import TxTimeoutException


PRE_WRITE_DELAY_MS = 10
__GBL__.__UART_MB__ = UART(CONFIG.MODBUS_UART_ID, CONFIG.Baud9600)


class rtuwire(object):

   def __init__(self):
      self.uinfo: uartinfo = None

   def set_uartinfo(self, uinfo: uartinfo):
      self.uinfo = uinfo
      __GBL__.__UART_MB__ = None
      __GBL__.__UART_MB__ = UART(CONFIG.MODBUS_UART_ID
         , baudrate=self.uinfo.baud
         , bits=self.uinfo.charbits
         , parity=self.uinfo.parity
         , stop=self.uinfo.stopbits
         , timeout=self.uinfo.timeout
         , timeout_char=self.uinfo.timeout_char)

   def send_receive(self, adu, maxTimeMS=48) -> [None, bytes, bytearray]:
      # print(f"\n-- send_receive --\n\tsending: {adu}")
      # -- clear rx buffer --
      __GBL__.__UART_MB__.read()
      # -- write to wire --
      time.sleep_ms(PRE_WRITE_DELAY_MS)
      byte_cnt = __GBL__.__UART_MB__.write(adu)
      # print(f"\tbytes sent: {byte_cnt}")
      # -- wait on response --
      try:
         return self.__read_response__()
      except TxTimeoutException:
         print("\nTxTimeoutException")
         return None
      except Exception as e:
         print(f"send_receive e: {e}")
         return None

   def __read_response__(self) -> bytearray:
      # - - - -
      # print("\t__read_response__")
      buff: bytearray = bytearray()
      # - - - -
      __tout__ = False
      def ontimeout(t):
         # print(f"t: {t}")
         nonlocal __tout__
         __tout__ = True
      # - - - -
      time.sleep_ms(25)
      # -- wait on the rx buffer; will run till tmr goes off --
      tmr: Timer = Timer(period=200, mode=Timer.ONE_SHOT, callback=ontimeout)
      while __GBL__.__UART_MB__.any() == 0:
         time.sleep_ms(self.uinfo.timeout_char)
         if __tout__:
            raise TxTimeoutException
      tmr.deinit()
      # -- stuff came --
      while __GBL__.__UART_MB__.any() > 0:
         buff.extend(__GBL__.__UART_MB__.read(1))
         time.sleep_ms(self.uinfo.timeout_char)
      # - - - -
      # print(f"\treceived: {buff}")
      return buff


import serial
import time
from radiolib import radioMsg



def ping_pong(ser: serial.Serial):
   pass


def ping_get_pong(ser: serial.Serial):
   ping = radioMsg.ping_msg(161, 0xff)
   print(f"ping: {ping}")
   ser.write(ping)
   ser.flush()

def send_msg_get_resp(ser: serial.Serial, barr: bytearray, max: int = 4):
   ser.reset_input_buffer()
   ser.reset_output_buffer()
   ser.write(barr)
   ser.flush()

   while ser.in_waiting == 0:
      print("waiting for response...")
      time.sleep(1)

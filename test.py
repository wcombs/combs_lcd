import sys, os, serial

scroll_on = "\x13"
scroll_off = "\x14"

ser = serial.Serial('/dev/cu.usbserial-00002006', 19200, timeout=1)
ser.write(scroll_off)

ser.write("stuff")

ser.close()

#!/usr/bin/env python3
import board
import busio
import serial
import adafruit_max9744
import struct

infile_path = "/dev/input/js0"
EVENT_SIZE = struct.calcsize("LhBB")
file = open(infile_path, "rb")
event = file.read(EVENT_SIZE)

#Initialize i2c bus
i2c = busio.I2C(board.SCL, board.SDA)

#Initialize Amplifier
amp= adafruit_max9744.MAX9744(i2c)


while event:
 print(struct.unpack("LhBB", event))
 (tv_msec, value, type, number) = struct.unpack("LhBB", event)
 if number == 12:
  print("lower volume")
  amp.volume_down()
 event = file.read(EVENT_SIZE)



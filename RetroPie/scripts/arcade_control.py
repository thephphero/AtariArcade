#!/usr/bin/python3

import time
from signal import pause
from gpiozero import LED, PWMLED, Button,  OutputDevice
from subprocess import check_call
import adafruit_max9744
import busio
from adafruit_extended_bus import ExtendedI2C as I2C

# Define constants
SCL_PIN=17
SDA_PIN=9
#Define LEDs
logo_light = LED(12)
coin_light = PWMLED(6)

#Define buttons
toggle1_button = Button(16)
toggle2_button = Button(26)
toggle3_button = Button(23)
power_button = Button(3)
coin_button = Button(11)

#Define relay
relay = OutputDevice(25, active_high=True, initial_value=False)

#Initialize i2c Bus
i2c =  I2C(3)
#Define amplifier
amp=adafruit_max9744.MAX9744(i2c)

def switch_logo_light_on():
	logo_light.on()
def switch_logo_light_off():
	logo_light.off()
def shutdown():
	switch_logo_light_off()
	print("Shutting down...")
	check_call(['sudo','poweroff'])
def toggle1_button_action():
	print("toggle 1")
	check_call(['echo','-n',' "QUIT"','|','nc','-u', '-w1', 'retropie.local', '55355'])
def toggle2_button_action():
	print("toggle 2")
	amp.volume_down()
	#check_call('echo -n "VOLUME_DOWN" | nc -u -w1 127.0.0.1 55355')
def toggle3_button_action():
	print("toggle 3")
	amp.volume_up()
	#check_call('echo -n "VOLUME_UP" | nc -u -w1 127.0.0.1 55355')
def coin_button_action():
	print("coin pressed")
	relay.toggle()
#light_button.when_pressed=switch_logo_light_on
#light_button.when_released=shutdown
try:
	#Coin pulse
	coin_light.pulse()

	#Set current states
	if power_button.is_pressed:
		logo_light.on()
		print("Logo lights On")
	else:
		print("Shutdown") 	
	# Assign event handlers
	power_button.when_pressed=switch_logo_light_on
	power_button.when_released=shutdown
	toggle1_button.when_pressed==toggle1_button_action
	toggle2_button.when_pressed=toggle2_button_action
	toggle3_button.when_pressed=toggle3_button_action
	coin_button.when_pressed=coin_button_action		
	# Keep script alive
	pause()

finally:
	pass

#!/usr/bin/env python3
from struct import *
from datetime import datetime
from gpiozero import CPUTemperature
import time
import subprocess
import paho.mqtt.client as mqtt
import socket
import json

mqtt_username = "celsoluiz81"
mqtt_password =  "Benicio08092017!"
mqtt_host = "homeassistant.local"
mqtt_port = 1883

#******************************************
# Callback function when the client successfully connects to the MQTT broker
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
#******************************************

def on_publish(client, userdata, mid, rc, properties):
    print("Published")
    pass

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds
    
#-------------------------------------------------------------------------------------------------------
# main function
def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(mqtt_host, mqtt_port)
    client.loop_start()

    while True:
      switch_state = True
      uptime = get_uptime()
      current_time = datetime.now()
      cpu = CPUTemperature()
      ip_address = socket.gethostbyname(socket.gethostname())
      # Publish config??
      config_payload = {
          "name": "Retropie Core Temperature",
          "state_topic": "homeassistant/sensor/retropie/state",
          "state_class": "measurement",
          "unit_of_measurement": "C",
          "device_class": "temperature",
          "value_template": "{{ value_json.temperature }}",
          "unique_id": "retropie",
          "device": {
            "identifiers": [
               "retropie"
            ],
            "name": "Retropie",
            "model": "Raspberry Pi 4",
            "manufacturer": "Raspberry Pi Foundation"
          },
          "icon": "mdi:gamepad-square",
          "platform": "mqtt"
      }
      client.publish(topic="homeassistant/sensor/retropie/config", payload=json.dumps(config_payload), qos=0, retain=False)

      # Publish State
      state_payload = {
	"temperature":cpu.temperature
	
      }
      topic1 = "homeassistant/sensor/retropie/state"
      client.publish(topic=topic1, payload=json.dumps(state_payload), qos=0, retain=False)

      # Publish State2
      topic2 = "homeassistant/sensor/retropie/game/state"
      client.publish(topic=topic2, payload=str(switch_state), qos=0, retain=False)
      

      time.sleep(6)

#---------------------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------






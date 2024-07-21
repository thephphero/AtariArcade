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
      config_temperature_payload = {
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
      client.publish(topic="homeassistant/sensor/retropie/config", payload=json.dumps(config_temperature_payload), qos=0, retain=False)

      config_uptime_payload = {
          "name": "Retropie Uptime",
          "state_topic": "homeassistant/sensor/retropie/state",
          "state_class": "measurement",
          "unit_of_measurement": "s",
          "device_class": "duration",
          "value_template": "{{ value_json.uptime }}",
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
      client.publish(topic="homeassistant/sensor/retropie/config", payload=json.dumps(config_uptime_payload),qos=0, retain=False)

      # Publish Temperature
      state_temperature_payload = {"temperature":cpu.temperature}
      state_temperature_topic = "homeassistant/sensor/retropie/state"
      client.publish(topic=state_temperature_topic, payload=json.dumps(state_temperature_payload), qos=0, retain=False)

      # Publish Uptime
      state_uptime_payload = {"uptime": uptime }
      state_uptime_topic = "homeassistant/sensor/retropie/state"
      client.publish(topic=state_uptime_topic, payload=json.dumps(state_uptime_payload), qos=0, retain=False)
      

      time.sleep(6)

#---------------------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------






import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
	if reason_code==0:
		#client.connected_flag=True
		print("Connect to Mosquitto OK")
	else:
		#client.bad_connection_flag=True
    		print(f"Bad connection returned code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
	client.subscribe("homeassistant/sensor/retropie")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	payload = json.loads(msg.payload)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#mqttc.connected_flag=False #create flag in class to be set in the on_connect callback
#mqttc.bad_connection_flag=False
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(username="celsoluiz81", password="Benicio08092017!")
mqttc.connect("homeassistant.local", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()


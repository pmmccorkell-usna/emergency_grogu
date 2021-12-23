import requests
import mqttClass
from time import sleep
from secrets import *

def homing(server):
	success = 0
	try:
		print('Connecting to ' + server)
		r = requests.get('http://'+server+'/rr_gcode?gcode=G28')
		print('shutdown sent')
		sleep(5)
		success = 1
	except:
		print('could not connect to ' + server)
		success = 0
	return success

def emergency_shutoff(server):
	success = 0
	try:
		print('Connecting to ' + server)
		r = requests.get('http://'+server+'/rr_gcode?gcode=M112%0AM999')
		print('shutdown sent')
		sleep(5)
		success = 1
	except:
		print('could not connect to ' + server)
		success = 0
	return success


def kill_it_all():
	global server1, server2
	if (not emergency_shutoff(server1)):
		sleep(1)
		emergency_shutoff(server2)

# Function to be called when topic is received.
# Must be in the format of func(topic,message)
def check_emergency(topic,message):
	print(topic)
	print(message.decode())
	if (message.decode()=='1'):
		kill_it_all()

# Dictionary of topics and associated callback functions for mqtt subscription.
# Each entry must be in the format of 'topic : callback_function'
subscription_dict = {
	ada_topic:check_emergency
}

def connect_ada():
	global ada
	# Instantiate paho-mqtt wrapper class
	ada = mqttClass.mqttClass(host_IP='io.adafruit.com',username=ada_user, key=ada_key, subscriptions = subscription_dict)
	ada.connect()
	# Registers the reconnect_ada function to be run when paho-mqtt detects a disconnect
	ada.client.on_disconnect = reconnect_ada

# If connection is lost, run this function to reconnect.
# Must be in the format of func(client,userdata,rc)
def reconnect_ada(client,userdata,rc):
	global ada
	ada.mqtt_terminate()
	sleep(3)
	connect_ada()


def main():
	connect_ada()
	while(1):
		# Everything is handled by interrupts and callbacks, so just keep the program alive with sleeps
		sleep(1)

if __name__ == '__main__':
	main()

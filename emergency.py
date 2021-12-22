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
	print('entered kill_it_all')
	server1 = '192.168.5.8'
	server2 = '10.60.5.236:8505'
	if (not emergency_shutoff(server1)):
		sleep(1)
		emergency_shutoff(server2)

def check_emergency(topic,message):
	print(topic)
	print(message.decode())
	if (message.decode()=='1'):
		kill_it_all()

subscription_dict = {
	ada_topic:check_emergency
}

def connect_ada():
	global ada, connected
	ada = mqttClass.mqttClass(host_IP='io.adafruit.com',username=ada_user, key=ada_key, subscriptions = subscription_dict)
	ada.connect()
	ada.client.on_disconnect = reconnect_ada
	connected = 1

def reconnect_ada(client,userdata,rc):
	global ada, connected
	connected = 0
	ada.mqtt_terminate()
	sleep(3)
	connect_ada()


def main():
	global connected
	connected = 0
	connect_ada()
	while(1):
		sleep(1)

if __name__ == '__main__':
	main()

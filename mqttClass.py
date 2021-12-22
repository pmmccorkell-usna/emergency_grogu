#
# Streamlined class of paho-mqtt for raspi
# US Naval Academy
# Robotics and Control TSD
# Patrick McCorkell
# April 2021
#

import paho.mqtt.client as MQTT
from random import randint
from json import dumps
from math import pi as pie

#USAGE:
# from mqttClass import mqttClass
# YOUR_DICTIONARY_OF_SUBSCRIPTIONS = {
	# 'topic1' : function_name_1,
	# 'topic2' : function_name_2,
	# ...
	# ...
	# ...
# }

# server = 'the broker's IP'
# mqtt = mqttClass(host_IP=server,subscriptions=YOUR_DICTIONARY_OF_SUBSCRIPTIONS)
#	  if connecting to Adafruit IO or 3rd party with username and pass:
#		   mqtt = mqttClass(host_IP=server, username='YOUR IO USER', key='YOUR IO KEY',subscriptions=YOUR_DICTIONARY_OF_SUBSCRIPTIONS)
# mqtt.connect()
# 
#
# To Subscribe:
#
# 1. Write a function with the code you want to execute when the subscription is received.
# def function_name_1(topic,message):
#	 ......
#	 your code for subscription
#	 ......
#
# 2. Create a dictionary['topic_name':function_name]
# Pass this dictionary at instantiation, subscriptions=YOUR_DICTIONARY_OF_SUBSCRIPTIONS)
#
#
#
# To Publish:
# mqtt.pub('topic','message')
#
#

class mqttClass:
	def __init__(self,host_IP='192.168.5.4',username=None,key=None,subscriptions=None):

		self.clientname="raspi"+str(randint(1000,9999))
		self.mqtt_server=host_IP
		self.is_connected=0
		self.client=MQTT.Client(self.clientname)
		# self.client.on_disconnect = self.reconnect
		if username is not None:
			self.client.username_pw_set(username,key)

		self.topic_list=set()

		topic_defaults={
			'test':self.test_function,
			'default':self.default_function
		}

		if type(subscriptions) is dict:
			self.topic_outsourcing = subscriptions
		else:
			self.topic_outsourcing = topic_defaults

		self.client.on_message = self.callback_handler

	def connect(self):
		while(not self.is_connected):
			print("Attempting connection to " + self.mqtt_server)
			self.client.connect(self.mqtt_server)
			print("Connected to "+self.mqtt_server)
			self.client.loop_start()
			print('loop start')
			self.is_connected=1
			self.auto_subscribe()
			sleep(1)

	def reconnect(self,client,userdata,rc):
		self.is_connected = 0
		print('connection lost: ' + str(rc))
		# rc is 0 when we programatically tell the client to disconnect; so ignore this case.
		if rc != 0:
			# while(not self.is_connected):
			sleep(1)
			print('reconnecting to ' + self.mqtt_server)
			# self.connect()
			client.reconnect()
			self.auto_subscribe()

	# Break connection to MQTT broker.
	# Called from within Matlab to properly deconstruct MQTT client.
	def mqtt_terminate(self):
		self.client.loop_stop()
		self.client.disconnect()
		self.is_connected=0
		print("Terminated python MQTT")

	def __str__(self):
		return str(self.mqtt_server)



	#####################################################################
	####################### SUBSCRIPTION HANDLING #######################
	#####################################################################

	def sub(self,topic):
		self.topic_list.add(topic)
		self.client.subscribe(topic)

	def auto_subscribe(self):
		# print(self.topic_outsourcing)
		for k in self.topic_outsourcing:
			self.sub(k)
			print('subscribed to ' + str(k))

	def test_function(self,top,msg):
		print()
		print('tes topic rx: '+str(top))
		print(msg)
		print()

	# Redirect from MQTT callback function.
	# Error checking.
	def default_function(self,top,whatever):
		print("PYTHON >> Discarding data: "+str(whatever)+".")
		print("No filter for topic "+str(top)+" discovered.")

	# Callback for MQTT subscriptions.
	# Called as Interrupt by paho-mqtt when a subscribed topic is received.
	# 
	def callback_handler(self,client,userdata,message):
		topicFunction=self.topic_outsourcing.get(message.topic,self.default_function)
		topicFunction(message.topic,message.payload)


	############################################################
	####################### PUBLISHING #########################
	############################################################

		
	def pub(self,topic,data):

		if type(data) is dict:
			msg = dumps(data)
		else:
			msg=data
		self.connect()
		
		# Publish json-ified msg to MQTT broker.
		self.client.publish(topic,msg)
		# print('published msg: '+dumps(msg) + ' on topic: '+dynamictopic)



from time import sleep

def test_function(msg):
	print(msg)
	print(msg.topic)
	print(msg.payload)

def debugging():
	print('debugging')
	subs = {
		'test':test_function
	}
	myserver = '127.0.0.1'
	debug_client = mqttClass(host_IP=myserver,subscriptions=subs)
	debug_client.connect()
	# debug_client.auto_subscribe()
	# for i in range(50):
	while(1):
		debug_client.publish('test',1235)
		sleep(0.5)

# debugging()

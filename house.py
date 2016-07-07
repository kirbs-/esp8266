import requests
import dht as DHT
from machine import Pin

class Reading(object):

	pin = 5
	temp_id = 8
	humidity_id = 14
	house_url = 'http://192.168.1.28'
	dht = DHT.DHT22(Pin(pin))

	# def __init__(self):
	# 	self.pin = 5
	# 	self.temp_id = 8
	# 	self.humidity_id = 14
	# 	self.house_url = 'http://192.168.1.28'
	# 	self.dht = DHT.DHT22(Pin(pin))


	def run(self):
		self.dht.measure()
		requests.post("{0}/sensors/{1}/readings".format(self.house_url, self.temp_id), json=self.temp_json())
		requests.post("{0}/sensors/{1}/readings".format(self.house_url, self.humidity_id), json=self.humidity_json())

	def temp_json(self):
		return {'reading': {'value': self.convert_to_fahernheit(self.dht.temperature())}}

	def humidity_json(self):
		return {'reading': {'value': self.dht.humidity()}}

	def convert_to_fahernheit(self, val):
		return val * 1.8 + 32
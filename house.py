import requests
from machine import Pin
import time
import machine
import sys

class Reading(object):

	pin = 5
	temp_id = 15
	# humidity_id = 14
	house_url = 'http://192.168.1.28'
	dht = DHT.DHT22(Pin(pin))

	# def __init__(self):
	# 	self.pin = 5
	# 	self.temp_id = 8
	# 	self.humidity_id = 14
	# 	self.house_url = 'http://192.168.1.28'
	# 	self.dht = DHT.DHT22(Pin(pin))

	def post(self):
		self.dht.measure()
		temp_response = None
		humdity_response = None
		try:
			temp_response = (requests.post("{0}/sensors/{1}/readings.json".format(self.house_url, self.temp_id), 
						json=self.temp_json(), 
						headers={'Content-Type':'application/json'}))
		except NotImplementedError:
			pass
		except Exception as e:
			print(sys.print_exception(e))
			print("Error posting temp")
			if temp_response:
				print("{0}:{1}".format(temp_response.status_code, temp_response.reason))
			machine.reset()

		try:
			humdity_response = (requests.post("{0}/sensors/{1}/readings.json".format(self.house_url, self.humidity_id), 
						json=self.humidity_json(),
						headers={'Content-Type':'application/json'}))
		except NotImplementedError:
			pass
		except Exception as e:
			print(sys.print_exception(e))
			print("Error posting humidity")
			if humdity_response:
				print("{0}:{1}".format(humdity_response.status_code, humdity_response.reason))
			machine.reset()

	def temp_json(self):
		return {'reading': {'value': self.convert_to_fahernheit(self.dht.temperature())}}

	def humidity_json(self):
		return {'reading': {'value': self.dht.humidity()}}

	def convert_to_fahernheit(self, val):
		return val * 1.8 + 32

def parse(lines):
    yaml = {}
    for line in lines:
        if ':' in line:
            components = line.split(':')
            yaml[components[0].strip()] = components[1].strip()
    return yaml

def sync_time(minute):
	time_delta = (minute * 60) - (time.time() % (minute * 60))
	print("Sleeping for {} seconds to sync to {} minutes past the hour.". format(time_delta, minute))
	time.sleep(time_delta)


def run():
	sync_time(5)

	while True:
		try:
			reading = Reading()
			reading.post()
			print(reading.dht.temperature())
			reading = None
		except Exception as e:
			print(sys.print_exception(e))

		print("Sleeping...")
		# time.sleep(30)
		time.sleep(5 * 60)

import requests
from machine import Pin
import time
import machine
import sys
from sensors import DS18B20

class Reading(object):

	pin = 5
	temp_id = 15
	# humidity_id = 14
	house_url = 'http://192.168.1.28'

	def post(self, temperature):
		temp_response = None
		try:
			temp_response = (requests.post("{0}/sensors/{1}/readings.json".format(self.house_url, self.temp_id), 
						json=self.temp_json(temperature), 
						headers={'Content-Type':'application/json'}))
		except NotImplementedError:
			pass
		except Exception as e:
			print(sys.print_exception(e))
			print("Error posting temp")
			if temp_response:
				print("{0}:{1}".format(temp_response.status_code, temp_response.reason))
			machine.reset()

	def temp_json(self, temperature):
		return {'reading': {'value': self.convert_to_fahernheit(temperature)}}

	def convert_to_fahernheit(self, val):
		return val * 1.8 + 32

# def parse(lines):
#     yaml = {}
#     for line in lines:
#         if ':' in line:
#             components = line.split(':')
#             yaml[components[0].strip()] = components[1].strip()
#     return yaml

def sync_time(minute):
	time_delta = (minute * 60) - (time.time() % (minute * 60))
	print("Sleeping for {} seconds to sync to {} minutes past the hour.". format(time_delta, minute))
	time.sleep(time_delta)

def sleep(seconds):
	rtc = machine.RTC()
	rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
	rtc.alarm(rtc.ALARM0, seconds * 1000)
	machine.deepsleep()


def run():
	sync_time(1)
	ds = DS18B20(5)

	while True:
		try:
			reading = Reading()
			temperature = ds.temperature()
			reading.post(temperature)
			print(temperature)
			reading = None
		except Exception as e:
			print(sys.print_exception(e))

		print("Sleeping...")
		# time.sleep(30)
		# time.sleep(1 * 60)
		sleep(10)

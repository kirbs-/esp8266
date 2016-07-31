import onewire as o
import time
from machine import Pin

class DS18B20(object):

	def __init__(self, pin):
		self.pin = pin

		self.ow = o.OneWire(Pin(self.pin))
		self.ds = o.DS18B20(self.ow)
		self.roms = self.ds.scan()

	def temperature(self, rom_num=0):
		self.ds.convert_temp()
		time.sleep_ms(750)
		return self.ds.read_temp(self.roms[rom_num])
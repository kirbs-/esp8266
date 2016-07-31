import onewire as ow
import time
from machine import pin

class ds(object):

	def __init__(self, pin):
		self.pin = pin

		self.ow = o.OneWire(Pin(pin))
		self.ds = o.DS18B20(ow)
		self.roms = self.ds.scan()
		return self

	def temperature(self, rom_num=0):
		self.ds.convert_temp()
		time.sleep_ms(750)
		self.ds.read_temp(roms[rom_num])
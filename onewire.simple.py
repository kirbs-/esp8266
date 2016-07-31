import onewire as ow
import time
from machine import pin


class DS18B20:

def __init__(self, pin):
	self.pin = pin

	self.ow = o.OneWire(Pin(pin))
	self.ds = o.DS18B20(ow)
	self.roms = ds.scan()
	return self

def temperature(self, rom_num=0)
	ds.convert_temp()
	time.sleep_ms(750)
	ds.read_temp(roms[rom_num])
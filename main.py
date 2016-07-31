print('Starting up...')

import ntptime
import time

print('Sleeping for 10 seconds')
time.sleep(10)

print("Attempting to set time from ntp.")
# set time from ntp
for x in range(10):
	try:
		ntptime.settime()
		print("Time set.")
		break
	except:
		print("Unable to set time. Attempt {0}".format(x))
		time.sleep(5)

import house
house.run()
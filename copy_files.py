#import requests
#
#import usocket
file = 'https://raw.githubusercontent.com/kirbs-/esp8266/master/sensors/__init__.py'
response = request('GET', file)
#print(response.text)

with open('/sensors/__init__.py','w') as f:
    f.write(response.content)

#import os
#os.mkdir('/sensors')
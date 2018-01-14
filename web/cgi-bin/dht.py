#!/usr/bin/python
import sys
import Adafruit_DHT

print("Content-Type: text/plain\n")

sensor=Adafruit_DHT.AM2302
pin=3

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('{0:0.1f}C  {1:0.1f}%H'.format(temperature, humidity))
else:
    print('Failed to get reading.')

#!/usr/bin/python
import board
import adafruit_dht

print("Content-Type: text/plain\n")

dht=adafruit_dht.DHT22(board.D3)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
temperature = dht.temperature
humidity = dht.humidity

if humidity is not None and temperature is not None:
    print('{0:0.1f}C  {1:0.1f}%H'.format(temperature, humidity))
else:
    print('Failed to get reading.')

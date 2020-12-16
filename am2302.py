#!/usr/bin/python
import board
import adafruit_dht

dht=adafruit_dht.DHT22(board.D3)

temperature = dht.temperature
humidity = dht.humidity

if humidity is not None and temperature is not None:
    print('{0:0.1f}C  {1:0.1f}%H'.format(temperature, humidity))
else:
    print('Failed to get reading.')

#!/usr/bin/python
# HC-SR501

import RPi.GPIO as GPIO
import time
from time import gmtime, strftime

GPIO.setmode(GPIO.BOARD) #Set GPIO to pin numbering
pir = 8 #Assign pin 8 to PIR
led = 10 #Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output
print ("Sensor initializing . . .")
time.sleep(2) #Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")

try:
  while True:
    if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
      print ("Motion Detected!", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
      GPIO.output(led, True) #Turn on LED
      time.sleep(1) #Keep LED on for 4 seconds
      GPIO.output(led, False) #Turn off LED
      time.sleep(0.1)

except KeyboardInterrupt: #Ctrl+c
  pass #Do nothing, continue to finally

finally:
  GPIO.output(led, False) #Turn off LED in case left on
  GPIO.cleanup() #reset all GPIO

print ("Program ended")

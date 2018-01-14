#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys
import cgi

print("Content-Type: text/plain\n")

GPIO.setmode(GPIO.BOARD)# set the pins numbering mode

# Select the GPIO pins used for the encoder K0-K3 data inputs
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

GPIO.setup(18, GPIO.OUT) # Select the signal to select ASK/FSK
GPIO.setup(22, GPIO.OUT) # Select the signal used to enable/disable the modulator

GPIO.output (22, False)  # Disable the modulator by setting CE pin lo

# Set the modulator to ASK for On Off Keying by setting MODSEL pin lo
GPIO.output (18, False)

arg = cgi.FieldStorage()['msg'].value
print(arg)

bits = []

for char in arg:
  bits.append(char == "1")
 
loops = len(bits) / 4

if loops >= 0:
  for i in range(loops):
    print(i, bits[4*i : 4*i + 4])

    # Set K0-K3
    GPIO.output (11, bits[4*i + 3])
    GPIO.output (15, bits[4*i + 2])
    GPIO.output (16, bits[4*i + 1])
    GPIO.output (13, bits[4*i + 0])

    time.sleep(0.1)         # let it settle, encoder requires this
    GPIO.output (22, True)  # Enable the modulator
    time.sleep(0.25)        # keep enabled for a period
    GPIO.output (22, False) # Disable the modulator

GPIO.cleanup()

print("OK")

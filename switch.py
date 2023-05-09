import sys
import time

import RPi.GPIO as GPIO

if __name__ == "__main__":
  try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN)
    last_value = True
    while True:
      input_value = GPIO.input(26)
      if input_value != last_value:
        print(f"switched! {not input_value}")
      last_value = input_value
      time.sleep(1) # Loop every second
  finally:
    GPIO.cleanup()
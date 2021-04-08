import sys

import RPi.GPIO as GPIO

def led(state):
  GPIO.setmode(GPIO.BOARD)
  led = 10
  GPIO.setup(led, GPIO.OUT)

  try:
    GPIO.output(led, state)
  except:
    pass

if __name__ == "__main__":
  try:
    led(sys.argv[1] == "1")
  finally:
    GPIO.cleanup()
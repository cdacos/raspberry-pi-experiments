import datetime
from datetime import datetime
import time

import energie
import utils

try:
  import board
  import adafruit_dht
  import RPi.GPIO as GPIO
  IS_A_PI = True
except:
  print('not a raspberry pi')
  IS_A_PI = False


def record_climate(dht, now):
  temperature = -999
  humidity = -999
  for i in range(0, 30):
    try:
      temperature = dht.temperature if IS_A_PI else -98
      humidity = dht.humidity if IS_A_PI else -97
      if humidity is not None and temperature is not None:
        break
    except RuntimeError as error:
      # Errors happen fairly often, DHT's are hard to read, just keep going
      print(error.args[0])
      time.sleep(2.0)
    except Exception as error:
      if IS_A_PI:
        dht.exit()
      raise error

  if temperature > -999 and humidity > -999:
    utils.post_climate(now, temperature, humidity)

  return temperature

dht = {}

if IS_A_PI:
  dht = adafruit_dht.DHT22(board.D3)

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(26, GPIO.IN)

recording_seconds = 0
last_switch_value = True
heater_off = False
heater_auto_off_level = 24
first_run = True

while True:
  now = datetime.utcnow()

  if recording_seconds >= 59:
    temperature = record_climate(dht, now)

    if not heater_off and temperature > heater_auto_off_level:
      print('Warm, so heater off!', temperature)
      energie.message('0110')
      heater_off = True
    elif heater_off and temperature < heater_auto_off_level:
      heater_off = False

    if now.hour >= 22 and now.minute < 1:
      print('Late, so lights off!')
      energie.message('0111')

    recording_seconds = 0
  recording_seconds = recording_seconds + 0.1

  # Lights physical switch. Look for toggle:
  if IS_A_PI:
    input_switch_value = GPIO.input(26)
  else:
    input_switch_value = 0

  if first_run:
    print('Switch is currently', input_switch_value)
    last_switch_value = input_switch_value

  if input_switch_value != last_switch_value:
    # toggle energie lights
    print('Switch!', input_switch_value)
    energie.message('0111', toggle=True)
    utils.post_log(now, 'Switch!')
    last_switch_value = input_switch_value

  first_run = False

  time.sleep(0.1) # Loop every second

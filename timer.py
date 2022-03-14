import datetime
import time
import board
import adafruit_dht

import RPi.GPIO as GPIO

import energie
import utils


def record_climate(dht, conn, now):
  temperature = -999
  humidity = -999
  for i in range(0, 30):
    try:
      temperature = dht.temperature
      humidity = dht.humidity
      if humidity is not None and temperature is not None:
        break
    except RuntimeError as error:
      # Errors happen fairly often, DHT's are hard to read, just keep going
      print(error.args[0])
      time.sleep(2.0)
    except Exception as error:
      dht.exit()
      raise error

  conn.execute('INSERT INTO climate (measured_on, temperature, humidity) VALUES(?, ?, ?)', (now.isoformat(), temperature, humidity))
  conn.commit()
  return temperature


dht = adafruit_dht.DHT22(board.D3)
recording_seconds = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
last_switch_value = True
heater_off = False
heater_auto_off_level = 22

while True:
  now = datetime.datetime.utcnow()

  if recording_seconds >= 59:
    conn = utils.get_conn()
    temperature = record_climate(dht, conn, now)

    if not heater_off and temperature > heater_auto_off_level:
      print('Warm, so heater off!', temperature)
      energie.message('0110', conn)
      heater_off = True
    elif heater_off and temperature < heater_auto_off_level:
      heater_off = False

    if now.hour >= 22 and now.minute < 1:
      print('Late, so lights off!')
      energie.message('0111', conn)

    conn.close()
    recording_seconds = 0
  recording_seconds = recording_seconds + 1

  # Lights physical switch. Look for toggle:
  input_switch_value = GPIO.input(26)
  if input_switch_value != last_switch_value:
    # toggle energie lights
    conn = utils.get_conn()
    energie.message('0111', conn, toggle=True)
    conn.execute('INSERT INTO log (created_on, message) VALUES(?, ?)', (now.isoformat(), 'Switch!'))
    conn.commit()
    conn.close()
    last_switch_value = input_switch_value

  time.sleep(1) # Loop every second

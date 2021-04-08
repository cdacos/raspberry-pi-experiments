import datetime
import time
import board
import adafruit_dht

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

while True:
  now = datetime.datetime.utcnow()

  if recording_seconds >= 59:
    conn = utils.get_conn()
    temperature = record_climate(dht, conn, now)

    if temperature > 22:
      print('Warm, so heater off!', temperature)
      energie.message('0110', conn)

    if now.hour >= 22 and now.minute < 1:
      print('Late, so lights off?')
      energie.message('0111', conn)

    conn.close()
    recording_seconds = 0
  recording_seconds = recording_seconds + 1

  
   
  time.sleep(1) # Loop every second

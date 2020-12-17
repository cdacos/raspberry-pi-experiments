import datetime
import time
import board
import adafruit_dht
import sqlite3
import os.path

temperature = -999
humidity = -999
dht = adafruit_dht.DHT22(board.D3)

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

now = datetime.datetime.utcnow().isoformat()

dbpath = '/var/log/raspberry-pi-experiments/data.db'
initialised = os.path.isfile(dbpath)

conn = sqlite3.connect(dbpath)

if not initialised:
    conn.execute('CREATE TABLE climate (id INTEGER PRIMARY KEY AUTOINCREMENT, measured_on DATETIME, temperature FLOAT, humidity FLOAT)')

conn.execute('INSERT INTO climate (measured_on, temperature, humidity) VALUES(?, ?, ?)', (now, temperature, humidity))
conn.commit()

conn.close()

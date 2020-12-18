import sqlite3
import os.path

def get_conn():
    dbpath = '/var/log/raspberry-pi-experiments/data.db'
    initialised = os.path.isfile(dbpath)

    conn = sqlite3.connect(dbpath)

    if not initialised:
        conn.execute('CREATE TABLE climate (id INTEGER PRIMARY KEY AUTOINCREMENT, measured_on DATETIME, temperature FLOAT, humidity FLOAT)')
        conn.execute('CREATE TABLE energie (id INTEGER PRIMARY KEY AUTOINCREMENT, messaged_on DATETIME, address TEXT)')
        conn.commit()

    return sqlite3.connect(dbpath)

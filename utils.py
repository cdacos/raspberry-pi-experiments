import os.path
import requests
import json
import datetime
from datetime import datetime

root_url = "http://192.168.174.1:8070"

def get_office_state():
    resp = requests.get(f'{root_url}/office')
    return json.loads(resp.text)

def post_device_state(now, address, switch):
    # conn.execute('INSERT INTO energie (messaged_on, address) VALUES(?, ?)', (now, address))
    response = requests.post(f'{root_url}/office/device', json={
        'event_date': now.isoformat(),
        'on': switch,
        'address': address
    })
    return response.status_code == 200

def post_climate(now, temperature, humidity):
    # conn.execute('INSERT INTO climate (measured_on, temperature, humidity) VALUES(?, ?, ?)', (now.isoformat(), temperature, humidity))
    response = requests.post(f'{root_url}/office/climate',  json={
        'measured_on': now.isoformat(),
        'temperature': temperature,
        'humidity': humidity
    })
    return response.status_code == 200

def post_log(now, message):
    # conn.execute('INSERT INTO log (created_on, message) VALUES(?, ?)', (now.isoformat(), message))
    response = requests.post(f'{root_url}/office/log',  json={
        'created_on': now.isoformat(),
        'message': message
    })
    return response.status_code == 200

from flask import render_template, redirect, request
from app import app

from datetime import datetime

import utils
import energie

@app.route('/')
@app.route('/index')
def index():
    conn = utils.get_conn()
    cur = conn.cursor()

    cur.execute('SELECT measured_on, temperature, humidity FROM climate ORDER BY id DESC LIMIT 1')
    latest_climate = cur.fetchall()
    climate = {'date': datetime.fromisoformat(latest_climate[0][0]), 'temperature': latest_climate[0][1], 'humidity': latest_climate[0][2]}

    cur.execute('SELECT address, MAX(messaged_on) FROM energie GROUP BY address')
    energie_messages = cur.fetchall()
    min_date = datetime(1, 1, 1)
    lights = {'on': min_date, 'off': min_date}
    heater = {'on': min_date, 'off': min_date}
    for (address, date) in energie_messages:
        date = datetime.fromisoformat(date)
        if address == '1111':
            lights['on'] = date
        elif address == '0111':
            lights['off'] = date
        elif address == '1110':
            heater['on'] = date
        elif address == '0110':
            heater['off'] = date
        else:
            print('Unknown address: ', address)
    lights['state'] = lights['on'] > lights['off']
    heater['state'] = heater['on'] > heater['off']

    conn.close()

    return render_template('index.html', title='Garden Office', climate=climate, lights=lights, heater=heater)

@app.route('/lights')
def lights():
    return toggle_switch('111')

@app.route('/heater')
def heater():
    return toggle_switch('110')

def toggle_switch(device_address):
    current_state = request.args.get('state') == 'True' or False
    address = ('0' if current_state else '1') + device_address
    conn = utils.get_conn()
    energie.message(address, conn)
    conn.close()
    return redirect('/#' + address)
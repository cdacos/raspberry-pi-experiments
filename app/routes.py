from flask import render_template, redirect, request
from app import app

from datetime import datetime

import utils
import energie

@app.route('/')
@app.route('/index')
def index():
    office_state = utils.get_office_state()

    devices = office_state['devices']
    climate = office_state['climate']

    lights = {}
    heater = {}

    for device in devices:
        if device['address'] == '111':
            lights['event_date'] = device['event_date']
            lights['state'] = device['on']
        elif device['address'] == '110':
            heater['event_date'] = device['event_date']
            heater['state'] = device['on']
        else:
            print('Unknown address: ', address)

    return render_template('index.html', title='Garden Office', climate=climate, lights=lights, heater=heater)

@app.route('/lights')
def lights():
    return toggle_switch('111')

@app.route('/heater')
def heater():
    return toggle_switch('110')

def toggle_switch(address):
    current_state = request.args.get('state') == 'True' or False
    instruction = ('0' if current_state else '1') + address
    energie.message(instruction)

    # Turning on the heating?
    autoLightsEnabled = False
    if autoLightsEnabled and instruction == '1110':
        # When turning on the heating, turn on the lights
        energie.message('1111')

    return redirect('/#' + address)

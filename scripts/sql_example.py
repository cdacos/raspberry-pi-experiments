from datetime import datetime

import utils

conn = utils.get_conn()
cur = conn.cursor()

cur = conn.cursor()

cur.execute('SELECT measured_on, temperature, humidity FROM climate ORDER BY id DESC LIMIT 1')
latest_climate = cur.fetchall()
climate = {'date': latest_climate[0][0], 'temperature': latest_climate[0][1], 'humidity': latest_climate[0][2]}

cur.execute('SELECT address, MAX(messaged_on) FROM energie GROUP BY address')
energie_messages = cur.fetchall()
lights = {'on': None, 'off': None}
heater = {'on': None, 'off': None}
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
min_date = datetime(1, 1, 1)
lights['state'] = (lights['on'] or min_date) > (lights['off'] or min_date)
heater['state'] = (heater['on'] or min_date) > (heater['off'] or min_date)

conn.close()

print(climate)
print(lights)
print(heater)

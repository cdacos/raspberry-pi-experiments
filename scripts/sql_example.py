import utils

conn = utils.get_conn()
cur = conn.cursor()
cur.execute('SELECT measured_on, temperature, humidity FROM climate ORDER BY id DESC LIMIT 1')
rows = cur.fetchall()
print(rows)
conn.close()
print({'date': rows[0][0], 'temperature': rows[0][1], 'humidity': rows[0][2]})
import sqlite3
import os

lat = list()
with open('latitude.dat', 'r') as lats:
    lat = lats.read().split('\n')

with open('longitude.dat', 'r') as lons:
    lon = lons.read().split('\n')

with open('dates.dat', 'r') as dates:
    tmp = [i[1:-1] for i in dates.read().split('\n')]

base = os.path.abspath(os.path.join('.', os.pardir))
conn = sqlite3.connect(base+'/firstsite/finder/static/finder/log.sqlite3')
cc = conn.cursor()
cc.execute('''CREATE TABLE IF NOT EXISTS log
                      (ID INTEGER PRIMARY KEY, IP TEXT, puerto TEXT, latitud TEXT, longitud TEXT, tiempo TEXT)''')
conn.commit()

for i in range(0, len(lat)):
    sent_data = ('9000', '192.168.1.1', lat[i], lon[i], tmp[i])
    cc.execute('''INSERT INTO log VALUES(NULL,?,?,?,?,?)''', sent_data)
conn.commit()

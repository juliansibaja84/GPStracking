import gpxpy
import gpxpy.gpx
import sqlite3
import os

# Parsing an existing file:
# -------------------------

gpx_file = open('data2.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

base = os.path.abspath(os.path.join('.', os.pardir))
conn = sqlite3.connect(base+'/firstsite/finder/static/finder/log.sqlite3')
cc = conn.cursor()
cc.execute('''CREATE TABLE IF NOT EXISTS truck2
                      (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT, longitud TEXT)''')
conn.commit()


for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lat = '+' + str(point.latitude)
            lon = str(point.longitude)
            if(abs(point.longitude) < 100):
                lon = str(point.longitude)[0] + '0' + str(point.longitude)[1:]
            time = str(point.time)
            while(len(lat) > 9):
                lat = lat[0:-1]
            while(len(lat) < 9):
                lat += '0'
            while(len(lon) > 9):
                lon = lon[0:-1]
            while(len(lon) < 9):
                lon += '0'
            sent_data = (time, lat, lon)
            cc.execute('''INSERT INTO truck2 VALUES(NULL,?,?,?)''', sent_data)
            # print(str(lat) + ' ' + str(lon) + ' ' + str(time))
conn.commit()

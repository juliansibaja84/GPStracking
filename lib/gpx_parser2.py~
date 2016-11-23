import gpxpy
import gpxpy.gpx
import sqlite3
import os
from time import sleep
import random
# Parsing an existing file:

gpx_file = open('data3.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

base = os.path.abspath(os.path.join('.', os.pardir))
conn = sqlite3.connect(base+'/firstsite/finder/static/finder/log.sqlite3')
cc = conn.cursor()
cc.execute('''CREATE TABLE IF NOT EXISTS truck2
                      (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT, longitud TEXT)''')
cc.execute('CREATE TABLE IF NOT EXISTS data2 (ID INTEGER PRIMARY KEY, taskid TEXT, datetime TEXT, val TEXT)')
conn.commit()

counter2 = 0
lock2 =1
delta2 = 1
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lat = '+' + str(point.latitude)
            lon = str(point.longitude)
            if(abs(point.longitude) < 100):
                lon = str(point.longitude)[0] + '0' + str(point.longitude)[1:]
            time = str(point.time)
            time = time[0:19]
            while(len(lat) > 9):
                lat = lat[0:-1]
            while(len(lat) < 9):
                lat += '0'
            while(len(lon) > 9):
                lon = lon[0:-1]
            while(len(lon) < 9):
                lon += '0'
            sent_data = (time, lat, lon)
            if counter2 == 22 and lock2 == 3:
                delta2 = -1
                lock2 = 4
            elif counter2 == 13 and lock2 == 4:
                delta2 = 1
                lock2 = 5
            elif counter2 == 18 and lock2 == 1:
                delta2 = -1
                lock2 = 2
            elif counter2 == 12 and lock2 == 2:
                delta2 = 1
                lock2 = 3
            elif counter2 == 15 and lock2 == 5:
                delta2 = -1
                lock2 = 6
            elif counter2 == 13 and lock2 == 6:
                delta2 = 1
                lock2 = 7
            elif counter2 == 15 and lock2 == 9:
                delta2 = -1
                lock2 = 10
            elif counter2 == 10 and lock2 == 8:
                delta2 = 1
                lock2 = 9
            elif counter2 == 30 and lock2 == 7:
                delta2 = -1
                lock2 = 8
            elif counter2 == 10 and lock2 == 10:
                delta2 = 1
                lock2 = 11
            elif counter2 == 22 and lock2 == 11:
                delta2 = -1
                lock2 = 2
            else:
                val = counter2 + random.uniform(1, 2)
                counter2 = counter2 + delta2
            data = [5, time, val]
            cc.execute('''INSERT INTO truck2 VALUES(NULL,?,?,?)''', sent_data)
            cc.execute('INSERT INTO data2 VALUES(null,?,?,?)', data)
            sleep(2)
            print(str(lat) + ' ' + str(lon) + ' ' + str(time))
            print(val)
            conn.commit()

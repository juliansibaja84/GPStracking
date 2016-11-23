import gpxpy
import gpxpy.gpx
import sqlite3
import os
from time import sleep
import random
# Parsing an existing file:

gpx_file = open('data.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

gpx_file2 = open('data3.gpx', 'r')
gpx2 = gpxpy.parse(gpx_file2)

vect = []
largo1 = 0
largo2 = 0

base = os.path.abspath(os.path.join('.', os.pardir))
conn = sqlite3.connect(base+'/firstsite/finder/static/finder/log.sqlite3')
cc = conn.cursor()

cc.execute('''CREATE TABLE IF NOT EXISTS truck1
                      (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT, longitud TEXT)''')
cc.execute('CREATE TABLE IF NOT EXISTS data1 (ID INTEGER PRIMARY KEY, taskid TEXT, datetime TEXT, val TEXT)')
cc.execute('''CREATE TABLE IF NOT EXISTS truck2
                      (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT, longitud TEXT)''')
cc.execute('CREATE TABLE IF NOT EXISTS data2 (ID INTEGER PRIMARY KEY, taskid TEXT, datetime TEXT, val TEXT)')
conn.commit()

counter = 0
lock = 1
delta = 1
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            largo1 = largo1+1
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
            if counter == 22 and lock == 1:
                delta = -1
                lock = 2
            elif counter == 13 and lock == 2:
                delta = 1
                lock = 3
            elif counter == 18 and lock == 3:
                delta = -1
                lock = 4
            elif counter == 12 and lock == 4:
                delta = 1
                lock = 5
            elif counter == 15 and lock == 5:
                delta = -1
                lock = 6
            elif counter == 13 and lock == 6:
                delta = 1
                lock = 7
            elif counter == 15 and lock == 7:
                delta = -1
                lock = 8
            elif counter == 10 and lock == 8:
                delta = 1
                lock = 9
            elif counter == 30 and lock == 9:
                delta = -1
                lock = 10
            elif counter == 10 and lock == 10:
                delta = 1
                lock = 11
            elif counter == 22 and lock == 10:
                delta = -1
                lock = 2
            else:
                val = counter + random.uniform(1, 2)
                counter = counter + delta
            data = [5, time, val]
            vect.append([sent_data, data, '1'])

counter2 = 0
lock2 =1
delta2 = 0.5
for track in gpx2.tracks:
    for segment in track.segments:
        for point in segment.points:
            largo2 = largo2+1
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
            vect.append([sent_data, data, '2'])
            # cc.execute('''INSERT INTO truck2 VALUES(NULL,?,?,?)''', sent_data)
            # cc.execute('INSERT INTO data2 VALUES(null,?,?,?)', data)
            # sleep(2)
            # print(str(lat) + ' ' + str(lon) + ' ' + str(time))
            # print(val)
            # conn.commit()

for i in range(0, len(vect)):
    cc.execute('''INSERT INTO truck1 VALUES(NULL,?,?,?)''', vect[i][0])
    cc.execute('INSERT INTO data1 VALUES(null,?,?,?)', vect[i][1])
    conn.commit()
    cc.execute('''INSERT INTO truck2 VALUES(NULL,?,?,?)''', vect[i+largo1][0])
    cc.execute('INSERT INTO data2 VALUES(null,?,?,?)', vect[i+largo1][1])
    conn.commit()
    print(str(lat) + ' ' + str(lon) + ' ' + str(time))
    print(vect[i][0])
    print(vect[i][1])
    print(vect[i][2])
    print(vect[i+largo1][0])
    print(vect[i+largo1][1])
    print(vect[i+largo1][2])
    sleep(2)
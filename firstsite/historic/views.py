from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import os
import sqlite3


def index(request):
    template = loader.get_template('historic/index.html')

    return HttpResponse(template.render())


def getPoints(request, lower='', upper=''):
    dictio = loadElements(lower, upper)
    return JsonResponse(dictio)


def getPointsT(request, latit='',longit='', lower='',upper=''):

    dictio = loadElementsT(lower, upper, latit, longit)
    return JsonResponse(dictio)


def loadElementsT(lower, upper, latitude, longitude):
    com1 = lower.replace('T', ' ')
    com2 = upper.replace('T', ' ')
    a = 0.0022
    limLatLow = str(float(latitude)-a)
    limLatHigh = str(float(latitude)+a)
    limLonLow = str(float(longitude)-a)
    limLonHigh = str(float(longitude)+a)
    limits = [limLatLow, limLatHigh, limLonLow, limLonHigh]
    lim_temp = 0
    if float(latitude) < 0:
        lim_temp = limits[0]
        limits[0] = limits[1]
        limits[1] = lim_temp
    if float(longitude) < 0:
        lim_temp = limits[2]
        limits[2] = limits[3]
        limits[3] = lim_temp

    lim=['0','0','0','0']; a = 0
    for limit in limits:
        if float(limit) >= 0:
            if float(limit)%10 < 1:
                lim[a] = "+0"+limit
            else:
                lim[a] = "+"+limit       
        else:
            if abs(float(limit))%10 < 1:
                lim[a] = "-00"+str((-1)*float(limit))
            elif abs(float(limit))%10 < 10:
                lim[a] = "-0"+str((-1)*float(limit))
            else:
                lim[a] = str(limit)
        a += 1
    conn, cc = createConnectionAndCursor()
    dat = cc.execute("SELECT * FROM (SELECT * FROM log WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "') as T WHERE latitud BETWEEN '"+lim[0]+"' AND '"+lim[1]+"' and longitud BETWEEN '"+lim[2]+"' AND '"+lim[3] + "'")
    dat = dat.fetchall()
    return constructDictionary(dat)

    


def loadElements(lower, upper):
    conn, cc = createConnectionAndCursor()
    com1 = lower.replace('T', ' ')
    com2 = upper.replace('T', ' ')
    dat = cc.execute("SELECT * FROM log WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "'")
    dat = dat.fetchall()
    return constructDictionary(dat)


def constructDictionary(list_of_sets):
    dictionary = dict()

    ips = [list_of_sets[x][1] for x in range(len(list_of_sets))]
    prt = [list_of_sets[x][2] for x in range(len(list_of_sets))]
    lat = [list_of_sets[x][3] for x in range(len(list_of_sets))]
    lon = [list_of_sets[x][4] for x in range(len(list_of_sets))]
    tmp = [list_of_sets[x][5] for x in range(len(list_of_sets))]

    dictionary['ips'] = ';'.join(ips)
    dictionary['prt'] = ';'.join(prt)
    dictionary['lat'] = ';'.join(lat)
    dictionary['lon'] = ';'.join(lon)
    dictionary['tmp'] = ';'.join(tmp)

    return dictionary


def createConnectionAndCursor():
    b = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(b + '/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute(
        '''
        CREATE TABLE IF NOT EXISTS log
        (ID INTEGER PRIMARY KEY, IP TEXT, puerto TEXT, latitud TEXT,
        longitud TEXT, tiempo TEXT)
        ''')
    return (conn, cc)

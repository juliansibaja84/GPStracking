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


def loadElements(lower, upper):
    conn, cc = createConnectionAndCursor()
    com1 = lower + " 00:00:00"
    com2 = upper + " 00:00:00"
    dat = cc.execute("SELECT * FROM log WHERE tiempo BETWEEN '" + com1 + "' and '" + com2 + "'")
    dat = dat.fetchall()
    print(dat)
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

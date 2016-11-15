from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import os
import sqlite3


def index(request):
    template = loader.get_template('finder/logger.html')
    return HttpResponse(template.render())


def req(request):
    dictio = loadElements()
    return JsonResponse(dictio)


def reqOne(request):
    dictio = loadElement()
    return JsonResponse(dictio)


def reqOneAnother(request):
    dictio = loadElementAnother()
    return JsonResponse(dictio)


def reqMany(request):
    dictio1 = loadElement()
    dictio2 = loadElementAnother()
    d = dict()
    d['tmp1'] = dictio1['tmp']
    d['tmp2'] = dictio2['tmp']
    d['lat1'] = dictio1['lat']
    d['lat2'] = dictio2['lat']
    d['lon1'] = dictio1['lon']
    d['lon2'] = dictio2['lon']
    return JsonResponse(d)


def reqOBD(request, truck='', code=''):
    conn, c = createConnectionAndCursorData()
    query = ["select val from ", " where taskid='", "' order by datetime desc limit 1"]
    if truck == 'truck1':
        dat1 = c.execute(query[0]+'data'+str(1)+query[1]+code+query[2])
        dat1 = dat1.fetchone()
        dat2 = ''
    elif truck == 'truck2':
        dat1 = c.execute(query[0]+'data'+str(2)+query[1]+code+query[2])
        dat1 = dat1.fetchone()
        dat2 = ''
    else:
        dat1 = c.execute(query[0]+'data'+str(1)+query[1]+code+query[2])
        dat1 = dat1.fetchone()
        dat2 = c.execute(query[0]+'data'+str(2)+query[1]+code+query[2])
        dat2 = dat2.fetchone()
    d = dict()
    d['val1'] = dat1
    d['val2'] = dat2
    return JsonResponse(d)


def loadElement():
    conn, cc = createConnectionAndCursor()
    dat = cc.execute('SELECT * FROM truck1 WHERE ID=(SELECT MAX(ID) FROM truck1)')
    dat = dat.fetchone()

    conn.close()

    d = dict()
    d['tmp'] = dat[1]
    d['lat'] = dat[2]
    d['lon'] = dat[3]

    return d


def loadElementAnother():
    conn, cc = createConnectionAndCursorAnother()
    dat = cc.execute('SELECT * FROM truck2 WHERE ID=(SELECT MAX(ID) FROM truck2)')
    dat = dat.fetchone()

    conn.close()
    d = dict()
    d['tmp'] = dat[1]
    d['lat'] = dat[2]
    d['lon'] = dat[3]

    return d


def createConnectionAndCursorData():
    b = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(b + '/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute('CREATE TABLE IF NOT EXISTS data' + str(1) + ' (ID INTEGER PRIMARY KEY, taskid TEXT, datetime TEXT, val TEXT)')
    cc.execute('CREATE TABLE IF NOT EXISTS data' + str(2) + ' (ID INTEGER PRIMARY KEY, taskid TEXT, datetime TEXT, val TEXT)')
    return (conn, cc)


def createConnectionAndCursor():
    b = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(b + '/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute('CREATE TABLE IF NOT EXISTS truck1 (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT,longitud TEXT)')
    return (conn, cc)


def createConnectionAndCursorAnother():
    b = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(b + '/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute('CREATE TABLE IF NOT EXISTS truck2 (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT,longitud TEXT)')
    return (conn, cc)

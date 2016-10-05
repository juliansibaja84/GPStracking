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

def loadElement():
    conn, cc = createConnectionAndCursor()
    dat = cc.execute('SELECT * FROM log WHERE ID=(SELECT MAX(ID) FROM log)')
    dat = dat.fetchone()
    
    d = dict()
    d['ips'] = dat[1]
    d['prt'] = dat[2]
    d['lat'] = dat[3]
    d['lon'] = dat[4]
    d['tmp'] = dat[5]

    return d

def loadElementAnother():
    conn, cc = createConnectionAndCursor()
    dat = cc.execute('SELECT * FROM log2 WHERE ID=(SELECT MAX(ID) FROM log)')
    dat = dat.fetchone()
    
    d = dict()
    d['ips'] = dat[1]
    d['prt'] = dat[2]
    d['lat'] = dat[3]
    d['lon'] = dat[4]
    d['tmp'] = dat[5]

    return d


def loadElements():
    conn, cc = createConnectionAndCursor()
    row = cc.execute('SELECT * FROM log ORDER BY ID')
    row = row.fetchall()
    d = constructDictionary(row)

    return d


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

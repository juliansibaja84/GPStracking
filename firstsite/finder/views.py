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

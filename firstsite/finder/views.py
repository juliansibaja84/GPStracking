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
    conn, cc = createConnectionAndCursorAnother()
    dat = cc.execute('SELECT * FROM log2 WHERE ID=(SELECT MAX(ID) FROM log2)')
    dat = dat.fetchone()
    
    d = dict()
    d['ips'] = dat[1]
    d['prt'] = dat[2]
    d['lat'] = dat[3]
    d['lon'] = dat[4]
    d['tmp'] = dat[5]

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

def createConnectionAndCursorAnother():
    b = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(b + '/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute(
        '''
        CREATE TABLE IF NOT EXISTS log2
        (ID INTEGER PRIMARY KEY, IP TEXT, puerto TEXT, latitud TEXT,
        longitud TEXT, tiempo TEXT)
        ''')
    return (conn, cc)

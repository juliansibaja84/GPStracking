from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from os.path import expanduser
import os
import sqlite3


def index(request):
    template = loader.get_template('historic/index.html')

    return HttpResponse(template.render())


@csrf_exempt
def statsRequests(request):
    template = loader.get_template('historic/stats/index.html')
    if request.method == 'GET':
        return HttpResponse(template.render)
    else:
        base = os.path.abspath(os.path.join('.', os.pardir))
        with open(base + "/firstsite/historic/static/historic/posts.txt", "a") as myfile:
            myfile.write('taskid: ' + request.POST['taskid'] + ' datetime: ' + request.POST['datetime'] + ' val: ' + request.POST['val'] + '\n')
        return HttpResponse('GOT IT')

def getPoints(request, lower='', upper=''):
    dictio = loadElements(lower, upper)
    return JsonResponse(dictio)


def getPointsT(request, latit='', longit='', lower='', upper=''):

    dictio = loadElementsT(lower, upper, latit, longit)
    return JsonResponse(dictio)


def loadElementsT(lower, upper, latitude, longitude):
    com1 = lower.replace('T', ' ')
    com2 = upper.replace('T', ' ')
    a = 0.0032
    limLatLow = str(float(latitude)-a)
    limLatHigh = str(float(latitude)+a)
    limLonLow = str(float(longitude)-a)
    limLonHigh = str(float(longitude)+a)
    limits = [limLatLow, limLatHigh, limLonLow, limLonHigh]

    if float(latitude) < 0:
        lim_temp = limits[0]
        limits[0] = limits[1]
        limits[1] = lim_temp
    if float(longitude) < 0:
        lim_temp = limits[2]
        limits[2] = limits[3]
        limits[3] = lim_temp

    lim = ['', '', '', '']
    if abs(float(limits[0])) < 10:
        lim[0] = '0'
    if abs(float(limits[1])) < 10:
        lim[1] = '0'
    if abs(float(limits[2])) < 100:
        lim[2] += '0'
        if abs(float(limits[2])) < 10:
            lim[2] += '0'
        if abs(float(limits[3])) < 100:
            lim[3] += '0'
            if abs(float(limits[3])) < 10:
                lim[3] += '0'

    if float(limits[0]) < 0:
        lim[0] = '-' + lim[0] + str(abs(float(limits[0])))
    else:
        lim[0] = '+' + lim[0] + str(abs(float(limits[0])))
    if float(limits[1]) < 0:
        lim[1] = '-' + lim[1] + str(abs(float(limits[1])))
    else:
        lim[1] = '+' + lim[1] + str(abs(float(limits[1])))
    if float(limits[2]) < 0:
        lim[2] = '-' + lim[2] + str(abs(float(limits[2])))
    else:
        lim[2] = '+' + lim[2] + str(abs(float(limits[2])))
    if float(limits[3]) < 0:
        lim[3] = '-' + lim[3] + str(abs(float(limits[3])))
    else:
        lim[3] = '+' + lim[3] + str(abs(float(limits[3])))

    lim = [limit[:10] for limit in lim]

    cmd = "SELECT * FROM log WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' AND latitud BETWEEN '"+lim[0]+"' AND '"+lim[1]+"' AND longitud BETWEEN '"+lim[2]+"' AND '"+lim[3] + "' ORDER BY tiempo"
    with open(expanduser('~') + '/cmds.txt', 'a') as file:
        file.write(cmd + '\n')
    conn, cc = createConnectionAndCursor()
    dat = cc.execute(cmd)
    dat = dat.fetchall()
    return constructDictionary(dat)


def loadElements(lower, upper):
    conn, cc = createConnectionAndCursor()
    com1 = lower.replace('T', ' ')
    com2 = upper.replace('T', ' ')
    dat = cc.execute("SELECT * FROM log WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' ORDER BY tiempo")
    dat = dat.fetchall()
    return constructDictionary(dat)


# Aquí empieza lo que concierne a el segundo camión
def getPointsAnother(request, lower='', upper=''):
    dictio = loadElementsAnother(lower, upper)
    return JsonResponse(dictio)


def getPointsTAnother(request, latit='', longit='', lower='', upper=''):
    dictio = loadElementsTAnother(lower, upper, latit, longit)
    return JsonResponse(dictio)


def loadElementsTAnother(lower, upper, latitude, longitude):
    com1 = lower.replace('T', ' ')
    com2 = upper.replace('T', ' ')
    a = 0.0032
    limLatLow = str(float(latitude)-a)
    limLatHigh = str(float(latitude)+a)
    limLonLow = str(float(longitude)-a)
    limLonHigh = str(float(longitude)+a)
    limits = [limLatLow, limLatHigh, limLonLow, limLonHigh]

    if float(latitude) < 0:
        lim_temp = limits[0]
        limits[0] = limits[1]
        limits[1] = lim_temp
    if float(longitude) < 0:
        lim_temp = limits[2]
        limits[2] = limits[3]
        limits[3] = lim_temp

    lim = ['', '', '', '']
    if abs(float(limits[0])) < 10:
        lim[0] = '0'
    if abs(float(limits[1])) < 10:
        lim[1] = '0'
    if abs(float(limits[2])) < 100:
        lim[2] += '0'
        if abs(float(limits[2])) < 10:
            lim[2] += '0'
        if abs(float(limits[3])) < 100:
            lim[3] += '0'
            if abs(float(limits[3])) < 10:
                lim[3] += '0'

    if float(limits[0]) < 0:
        lim[0] = '-' + lim[0] + str(abs(float(limits[0])))
    else:
        lim[0] = '+' + lim[0] + str(abs(float(limits[0])))
    if float(limits[1]) < 0:
        lim[1] = '-' + lim[1] + str(abs(float(limits[1])))
    else:
        lim[1] = '+' + lim[1] + str(abs(float(limits[1])))
    if float(limits[2]) < 0:
        lim[2] = '-' + lim[2] + str(abs(float(limits[2])))
    else:
        lim[2] = '+' + lim[2] + str(abs(float(limits[2])))
    if float(limits[3]) < 0:
        lim[3] = '-' + lim[3] + str(abs(float(limits[3])))
    else:
        lim[3] = '+' + lim[3] + str(abs(float(limits[3])))

    lim = [limit[:10] for limit in lim]

    cmd = "SELECT * FROM log2 WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' AND latitud BETWEEN '"+lim[0]+"' AND '"+lim[1]+"' AND longitud BETWEEN '"+lim[2]+"' AND '"+lim[3] + "' ORDER BY tiempo"
    with open(expanduser('~') + '/cmds.txt', 'a') as file:
        file.write(cmd + '\n')
    conn, cc = createConnectionAndCursorAnother()
    dat = cc.execute(cmd)
    dat = dat.fetchall()
    return constructDictionary(dat)


def loadElementsAnother(lower, upper):
    conn, cc = createConnectionAndCursorAnother()
    com1 = lower.replace('T', ' ')
    com2 = upper.replace('T', ' ')
    dat = cc.execute("SELECT * FROM log2 WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' ORDER BY tiempo")
    dat = dat.fetchall()
    return constructDictionary(dat)

# Aquí termina lo que concierne al segundo camión


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



# ---------------The real thing begins here--------------

@csrf_exempt
def savePos(request):
    lat = request.POST['lat']
    lon = request.POST['lon']
    time = request.POST['time']
    idT = request.POST['idT']
    lat = "+"+lat[0:2]+"."+lat[2:7]
    lon = "-"+lon[0:3]+"."+lon[3:8]
    time = time.replace("_"," ")
    
    data = (time,lat,lon)
    conn, cc = connectionDB(idT)
    cc.execute('INSERT INTO truck'+idT+' VALUES(null,?,?,?)', data)
    conn.commit()
    conn.close()
    print(lat)
    print(lon)
    return 0
    
def connectionDB(i):
    base = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(base+'/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute('CREATE TABLE IF NOT EXISTS truck'+i+' (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT,longitud TEXT)')
    return (conn, cc)
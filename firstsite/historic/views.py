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

    cmd = "SELECT * FROM truck1 WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' AND latitud BETWEEN '"+lim[0]+"' AND '"+lim[1]+"' AND longitud BETWEEN '"+lim[2]+"' AND '"+lim[3] + "' ORDER BY tiempo"
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
    dat = cc.execute("SELECT * FROM truck1 WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' ORDER BY tiempo")
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

    cmd = "SELECT * FROM truck2 WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' AND latitud BETWEEN '"+lim[0]+"' AND '"+lim[1]+"' AND longitud BETWEEN '"+lim[2]+"' AND '"+lim[3] + "' ORDER BY tiempo"
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
    dat = cc.execute("SELECT * FROM truck2 WHERE tiempo BETWEEN '" + com1 + "' AND '" + com2 + "' ORDER BY tiempo")
    dat = dat.fetchall()
    return constructDictionary(dat)

# Aquí termina lo que concierne al segundo camión


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


def constructDictionary(list_of_sets):
    dictionary = dict()
    tmp = [list_of_sets[x][1] for x in range(len(list_of_sets))]
    lat = [list_of_sets[x][2] for x in range(len(list_of_sets))]
    lon = [list_of_sets[x][3] for x in range(len(list_of_sets))]

    dictionary['tmp'] = ';'.join(tmp)
    dictionary['lat'] = ';'.join(lat)
    dictionary['lon'] = ';'.join(lon)


    return dictionary

# ---------------The real thing begins here--------------


@csrf_exempt
def savePos(request):
    print("hello")
    template = loader.get_template('historic/stats/index.html')
    if request.method == 'GET':
        return HttpResponse(template.render())
    else:
        lat = request.POST['lat']
        lon = request.POST['lon']
        time = request.POST['time']
        idT = request.POST['idT']
        lat = "+"+lat[0:2]+"."+lat[2:7]
        lon = "-"+lon[0:3]+"."+lon[3:8]
        time = time.replace("_", " ")
        
        data = (time, lat, lon)
        conn, cc = connectionDB(idT)
        cc.execute('INSERT INTO truck'+idT+' VALUES(null,?,?,?)', data)
        conn.commit()
        conn.close()
        return HttpResponse("")


def connectionDB(i):
    base = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(base+'/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute('CREATE TABLE IF NOT EXISTS truck'+i+' (ID INTEGER PRIMARY KEY, tiempo TEXT, latitud TEXT,longitud TEXT)')
    return (conn, cc)


def savePosCopy(vals):
    lat = vals['lat']
    lon = vals['lon']
    time = vals['datetime']
    idT = vals['idT']
    lat = "+"+lat
    time = time.replace("_", " ")

    data = (time, lat, lon)
    conn, cc = connectionDB(idT)
    cc.execute('INSERT INTO truck'+idT+' VALUES(null,?,?,?)', data)
    conn.commit()
    conn.close()


# esto de aquí abajo corresponde a las estadisticas
@csrf_exempt
def statsRequests(request):
    print("GOT IT")
    template = loader.get_template('historic/stats/index.html')
    if request.method == 'GET':
        return HttpResponse(template.render())
    else:
        if request.POST['taskid'] == '11':
            savePosCopy(request.POST)
            return HttpResponse('GOT IT')
        elif request.POST['taskid'] == '10':
            return HttpResponse('GOT IT')

        taskid = request.POST['taskid']
        val = request.POST['val']
        datetime = request.POST['datetime']
        datetime = datetime.replace("_", " ")
        # Guardar en base de datos
        idT = request.POST['idT']
        data = (taskid, datetime, val)
        conn, cc = createConnectionAndCursorData(idT)
        cc.execute('INSERT INTO data' + idT + ' VALUES(null,?,?,?)', data)
        conn.commit()
        conn.close()
        return HttpResponse('GOT IT')


def createConnectionAndCursorData(i):
    b = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(b + '/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute('CREATE TABLE IF NOT EXISTS data' + i + ' (ID INTEGER PRIMARY KEY, taskid TEXT, datetime TEXT, val TEXT)')
    return (conn, cc)


def getData(request, lower='', upper='', taskid='',idT=''):
    conn, cc = createConnectionAndCursorData(taskid)
    com1 = lower.replace('T', ' ')
    com2 = upper.replace('T', ' ')
    dat = cc.execute("SELECT * FROM data"+idT+" WHERE taskid="+taskid+" AND datetime BETWEEN '"+ com1 + "' AND '" + com2 + "' ORDER BY datetime")
    dat = dat.fetchall()

    dictionary = dict()
    tmp = [dat[x][2] for x in range(len(dat))]
    val = [dat[x][3] for x in range(len(dat))]

    time_dict = dateToList(com1,com2)
    vector_y = dataGrouper(time_dict, tmp, val)
    cont = 0
    for i in vector_y :
        if len(i)>1:
            suma = 0
            for j in i:
                suma = suma + int(j)
            vector_y[cont] = str(int(suma/len(i)))
        else:
            vector_y[cont] = vector_y[cont][0]
        cont += 1

    vector_x = str(time_dict['array'])
    vector_x = vector_x.split(',')
    if len(vector_x) > len(vector_y):
        diff = len(vector_x) - len(vector_y)
        vector_y.extend(['0']*diff)

    x=';'.join(vector_x)
    y=';'.join(vector_y)



    dictionary['x'] = x 
    dictionary['y'] = y
    dictionary['scale'] = time_dict['scale']

    print(dictionary)
    return JsonResponse(dictionary)


# -------------Aquí empieza el proceso de seleccíon de los datos a mostrar----------
# Definitions
MIN = 10


def dataGrouper(time_dict, data_time, data_value):
    # Data list is ordered by time
    # Data time has the format YYYY-MM-DD HH:MM:SS
    # Easy case is with days, hours and minutes
    data = list()
    scale = time_dict['scale']

    ini = 8
    fin = 10
    if scale == 'yhr':
        ini = 0
        fin = 4
    elif scale == 'mon':
        ini = 5
        fin = 7
    elif scale == 'hur':
        ini = 11
        fin = 13
    elif scale == 'min':
        ini = 14
        fin = 16

    # Merge data according to scale
    data_time, data_value = mergeData(data_time, data_value, ini, fin)

    for x in time_dict['array'].split(','):
        for i in range(0, len(data_time)):
            if int(x) == int(data_time[i]):
                data.append(data_value[i])
                break
            if int(x) < int(data_time[i]) + 1:
                data.append('0')
                break

    print('***********************************')
    return data


def mergeData(d_time, d_value, ini, fin):
    f_time = list()
    f_value = list()
    for x in d_time:
        check = False
        for i in range(0, len(d_time)):
            if x[ini:fin] not in f_time:
                check = True
                f_time.append(x[ini:fin])
                f_value.append([])
            if x[ini:fin] == d_time[i][ini:fin] and check:
                f_value[-1].append(d_value[i])
    print(f_time)
    print(f_value)
    return [f_time, f_value]


def dateToList(ini, fin):
    # Final list
    time_dict = dict()

    # Init and final dates YYYY-MM-DD HH:MM:SS
    dates = [ini, fin]

    # Break the dates in its basics components and store them away
    date_low = dict()
    date_high = dict()
    dates = [x.split(' ') for x in dates]

    date_low['yhr'] = dates[0][0][0:4]
    date_low['mon'] = dates[0][0][5:7]
    date_low['day'] = dates[0][0][8:]
    date_low['hur'] = dates[0][1][0:2]
    date_low['min'] = dates[0][1][3:5]
    date_low['sec'] = dates[0][1][6:]

    date_high['yhr'] = dates[1][0][0:4]
    date_high['mon'] = dates[1][0][5:7]
    date_high['day'] = dates[1][0][8:]
    date_high['hur'] = dates[1][1][0:2]
    date_high['min'] = dates[1][1][3:5]
    date_high['sec'] = dates[1][1][6:]

    # Get most significant time difference
    significance = 'yhr'
    for x in ['yhr', 'mon', 'day', 'hur', 'min', 'sec']:
        significance = x
        if date_low[x] != date_high[x]:
            break

    # Get numeric difference (for safeness take abs)
    diff = abs(int(date_high[significance]) - int(date_low[significance]))

    # Interpret difference
    # Output values are the same as significance
    time_list = list()

    # Date scheme
    ini = int(date_low[significance])
    fin = int(date_high[significance])
    scale = dateScheme(significance, time_list, diff, ini, fin)

    # Time scheme
    if not time_list:
        scale = timeScheme(significance, time_list, diff, ini, fin)

    time_dict['scale'] = scale
    time_dict['array'] = ','.join(str(x) for x in time_list)

    return time_dict


def dateScheme(significance, time_list, diff, ini, fin):
    time_list.extend(range(ini, fin + 1))
    return significance


def timeScheme(significance, time_list, diff, ini, fin):
    time_list.extend(range(ini, fin + 1))
    return significance

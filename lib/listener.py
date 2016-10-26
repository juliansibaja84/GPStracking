import socket
import sqlite3
import time
import datetime as dt
import math
import os


def databaseConnection():
    base = os.path.abspath(os.path.join('.', os.pardir))
    conn = sqlite3.connect(base+'/firstsite/finder/static/finder/log.sqlite3')
    cc = conn.cursor()
    cc.execute('''CREATE TABLE IF NOT EXISTS log
              (ID INTEGER PRIMARY KEY, IP TEXT, puerto TEXT, latitud TEXT,
              longitud TEXT, tiempo TEXT)''')
    return (conn, cc)

if __name__ == '__main__':

    method = 'udp'  # Reemplaza por tcp si lo requieres

    if method == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 9000
    sock.bind(("", port))

    # print('Esperando conexión')

    # Crear base de datos y habilitarla
    conn, cc = databaseConnection()
    conn.commit()
    conn.close()

    # Escuchar el puerto por un tiempo indefinido
    while 1:
        data, (r_ip, r_port) = sock.recvfrom(1024)

        # Procesar datos
        data = str(data, 'UTF-8')
        lon = ''
        lat = ''

        # Salir si los datos recogidos no son útiles
        if data[:4] != '>REV':
            continue

        lat = data[16:19] + '.' + data[19:24]
        lon = data[24:28] + '.' + data[28:33]

        # Obtener tiempo en un formato legible
        m, s = divmod(int(data[11:16]), 60)
        h, m = divmod(m, 60)

        time_high = "%d:%02d:%02d" % (h, m, s)
        time_low = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
        t = time_low + ' ' + time_high

        # Crear set de datos
        sent_data = (r_ip, r_port, lat, lon, t)

        # Hacer que se escriban los datos en una base de datos SQLite
        conn, cc = databaseConnection()
        cc.execute('''INSERT INTO log VALUES(NULL,?,?,?,?,?)''', sent_data)
        conn.commit()

        # La siguiente línea es para que puedas ver lo que hay en la base de
        # datos actualmente, para la versión final se omite
        #r = cc.execute('SELECT * FROM log WHERE ID=(SELECT MAX(ID) FROM log)')
        #r = r.fetchone()
        #print(r)
        print(lat)
        print(lon)
        print(sent_data)

import socket
import sqlite3
import time
import datetime
import os

method = 'udp'  # Reemplaza por tcp si lo requieres

if method == 'udp':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 9000
sock.bind(("", port))

print('Esperando conexión')

# Crear base de datos y habilitarla
conn = sqlite3.connect('log.sqlite3')
cc = conn.cursor()
cc.execute('''CREATE TABLE IF NOT EXISTS log
          (IP TEXT, puerto TEXT, latitud TEXT, longitud TEXT, tiempo TEXT)''')
conn.commit()

# Escuchar el puerto por un tiempo indefinido
while 1:
    data, (r_ip, r_port) = sock.recvfrom(1024)
    print(data)

    # Procesar datos
    data = str(data, 'UTF-8')
    lon = ''
    lat = ''

    # Crear set de datos
    sent_data = (r_ip, r_port, lat, lon, t)

    # Hacer que se escriban los datos en una base de datos SQLite
    cc.execute('''INSERT INTO log VALUES
        (?,?,?,?,?)''', sent_data)
    conn.commit()

    # La siguiente línea es para que puedas ver lo que hay en la base de datos
    # actualmente, para la versión final se omite
    row cc.execute('SELECT * FROM log ORDER BY tiempo DESC')
    print(row)

    os.system("python3 display.py")

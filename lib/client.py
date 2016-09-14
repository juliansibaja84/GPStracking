import socket
import time
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 9000)

tim = 70900
lat = 1101857
lon = 7483814

while(1):
    m = '>REV0519101' + str(tim) + '+' + str(lat) + '-0' + str(lon) + '00000012;ID=ENOMOTO<\r\n'
    try:
        sent = sock.sendto(bytes(m, 'UTF-8'), server_address)

    finally:
        print('Done')
    tim += 30
    lat -= 10
    lon += 70
    time.sleep(5)

sock.close()

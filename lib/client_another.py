import socket
import time
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('ennen.org', 9001)

tim = 60180
lat = 1099001
lon = 7482180

m = '>REV0519101' + str(tim) + '+' + str(lat) + '-0' + str(lon) + '00000012;ID=ENOMOTO<\r\n'
try:
    sent = sock.sendto(bytes(m, 'UTF-8'), server_address)
except:
	print("ERROR")

finally:
    print('Done')

sock.close()

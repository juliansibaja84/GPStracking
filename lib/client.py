import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('ennen.org', 9000)
message = '>REV051910172678+1102001-0748510200000012;ID=ENOMOTO<\r\n'

try:
    sent = sock.sendto(bytes(message, 'UTF-8'), server_address)

finally:
    sock.close()

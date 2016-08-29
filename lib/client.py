import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 9000)
message = '>REV051910172698+1102033-0748509300000012;ID=ENOMOTO<\r\n'

try:
    sent = sock.sendto(bytes(message, 'UTF-8'), server_address)

finally:
    sock.close()

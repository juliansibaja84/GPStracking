import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

<<<<<<< HEAD
server_address = ('localhost', 9000)
message = '>REV051910172626+1099006-0748269000000012;ID=ENOMOTO<\r\n'
=======
server_address = ('ennen.org', 9000)
message = '>REV051910172632+1099000-0748272100000012;ID=ENOMOTO<\r\n'
>>>>>>> 939d7e6c939ffbedaed3f0c5b905cb3c6ef1eb15

try:
    sent = sock.sendto(bytes(message, 'UTF-8'), server_address)

finally:
    sock.close()

import socket
import json
import sys

MESSAGE_SIZE = 4046

def send_command(obj):
    try:
        meta = "Sending:" + str(sys.getsizeof(obj))
        print(meta)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 9999)
        sock.connect(server_address)
        sock.sendall(meta.encode('utf-8'))
        response = sock.recv(MESSAGE_SIZE)
        print(response.decode('utf-8'))
        sock.send(obj)
    finally:
        sock.close()

obj = "some random test data\n" * 409600

message = obj.encode('utf-8')

send_command(message)

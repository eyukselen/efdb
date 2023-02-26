import socket
import json
import sys
from datetime import datetime


MESSAGE_SIZE = 4046

def timeit(f):
    def inn(*args):
        toc = datetime.now()
        result = f(*args)
        tic =  datetime.now()
        print(tic-toc)
        return result
    return inn

@timeit
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

# raw:
obj = "some random test data\n" * 50609600 
message = obj.encode('utf-8')

send_command(message)






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
        meta = {"name": "file_1",
                "size": str(sys.getsizeof(obj))
        }
        metas = json.dumps(meta)
        print(metas)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 9999)
        sock.connect(server_address)
        # send meta data and wait for ready message
        sock.sendall(metas.encode('utf-8'))
        response = sock.recv(MESSAGE_SIZE).decode('utf-8')
        if response == "ready":
            print('Server', response)
            sock.sendall(obj)
        else:
            print('server not ready')
    finally:
        sock.close()

# raw:
obj = "some random test data" 
message = obj.encode('utf-8')
obj2 = bytearray(b'some random test data')

send_command(message)
print(sys.getsizeof(obj))
print(sys.getsizeof(message))
print(sys.getsizeof(obj2))
print(type(message))
print(type(obj2))





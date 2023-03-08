import socket
import sys
from datetime import datetime
import json 

ip_address='localhost'
port=9999
server_address = (ip_address, port)


MESSAGE_SIZE = 4046 


# waits for conn at accept() and not proceed
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)
newSocket, address = sock.accept()
receivedData = newSocket.recv(MESSAGE_SIZE).decode('utf-8')
meta = json.loads(receivedData)
# print(mesg, size)
toc = datetime.now()
print('Starting receiving...' + meta['name'] + ' of ' + meta['size'] + ' bytes\n')
newSocket.send("ready".encode('utf-8'))
data = bytearray()
while True:
    buff = newSocket.recv(MESSAGE_SIZE)
    if not buff:
        break
    data.extend(buff)
print('size of received bytes:' + str(sys.getsizeof(data)))
print(data)
final_msg = "received:" + str(sys.getsizeof(data))
newSocket.send(final_msg.encode('utf-8'))
tic =  datetime.now()
print(tic-toc)
print( "=" + data.decode('utf-8') + "=")
print( sys.getsizeof(data.decode('utf-8')))


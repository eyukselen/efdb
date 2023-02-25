import socket
import sys
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
mesg, size = receivedData.split(':')
# print(mesg, size)
print('Starting receiving...' + size + ' bytes\n')
newSocket.send("Server ready!".encode('utf-8'))
data = bytes()
while True:
    buff = newSocket.recv(MESSAGE_SIZE)
    if not buff:
        break
    data += buff
print('size of received bytes:' + str(sys.getsizeof(data)))
# print(data.decode('utf-8'))


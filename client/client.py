import socket
import json

# with open('./data_file.json') as f:
#     json_file = json.load(f)

class Client:
    def __init__(self, ip_address='localhost', port=9999) -> None:
        self.server_address = (ip_address, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.connect(self.server_address)
        finally:
            pass    
        
    def disconnect(self):
        self.sock.close()


    def send_command(self, cmd_dict, data=None):
        res = None
        try:
            self.connect()
            message = json.dumps(cmd_dict).encode('utf-8')
            self.sock.sendall(message)
            received = self.sock.recv(4096)
            res = received.decode()
        finally:
            self.disconnect()
        return res




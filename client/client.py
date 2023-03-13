import socket
import json

# with open('./data_file.json') as f:
#     json_file = json.load(f)

class Client:
    def __init__(self, ip_address='localhost', port=9999) -> None:
        self.server_address = (ip_address, port)
        pass

    def send_command(self, cmd_dict, data=None):
        res = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.server_address)
            message = json.dumps(cmd_dict).encode('utf-8')
            sock.sendall(message)
            received = sock.recv(4096)
            res = received.decode()
        finally:
            sock.close()
        return res




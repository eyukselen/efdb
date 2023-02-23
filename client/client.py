import socket
import json

with open('./data_file.json') as f:
    json_file = json.load(f)


def send_command(cmd_dict, data=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 9999)
        sock.connect(server_address)
        message = json.dumps(cmd_dict).encode('utf-8')
        sock.sendall(message)
        received = sock.recv(4096)
        print(received.decode())
    finally:
        sock.close()


send_command({"action": "get_doc", "path": "bucket1", "name": "doc1"})
send_command({"action": "put_doc", "path": "bucket1", "name": "doc1",
              "data": "This is a sample data"})
send_command({"action": "put_doc", "path": "bucket1", "name": "doc0",
              "data": "This is a sample data"})
send_command({"action": "del_doc", "path": "bucket1", "name": "doc1"})
send_command({"action": "get_doc", "path": "bucket1", "name": "doc0"})

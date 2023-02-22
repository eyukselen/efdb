import socket
import json

with open('./data_file.json') as f:
    json_file = json.load(f)


def send_command(cmd_dict, data=None):
    try:
        # Send data
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 9999)
        sock.connect(server_address)
        message = json.dumps(cmd_dict).encode('utf-8')
        sock.sendall(message)
        received = sock.recv(4096)
        print(received.decode())
    finally:
        sock.close()


send_command({"action": "get_doc", "name": "sample_table"})
send_command({"action": "put_doc", "name": "sample_table",
              "data": "This is a sample data"})
send_command({"action": "put_doc", "name": "sample_table2",
              "data": "This is a sample data"})
send_command({"action": "del_doc", "name": "sample_table2"})

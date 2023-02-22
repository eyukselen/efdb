import json
import os
import socket
import logging


WORKING_PATH = os.getcwd()
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
EFDB_PATH = MODULE_PATH + "/efdb_data"
NUMBER_OF_CLIENTS = 5
MESSAGE_SIZE = 4096
LOG_PATH = MODULE_PATH + '/log'  # log folder
LOG_FILE = LOG_PATH + '/server.log'  # log file


def create_path_if_not_exist(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    return 'Checked:' + folder_path


paths_to_check = [EFDB_PATH, LOG_PATH, ]
paths_to_check = list(map(create_path_if_not_exist, paths_to_check))

# region logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO,
                    filename=LOG_FILE,
                    filemode='a')
server_log = logging.getLogger('server')
server_log.info('Server Initializing ...')
# endregion

server_log.info(paths_to_check)


class RequestHandler:
    def __init__(self, logger, socket, address, request, ) -> None:
        self.request = request
        self.socket = socket
        self.address = address
        self.db_ops = DbOps(logger)
        self.logger = logger

    def _process(self):
        self.logger.info(self.request)
        response = self.db_ops.process_message(self.request)
        # response = 'HTTP/1.0 200 OK\n\nSuccess!'
        self.socket.sendall(response.encode())
        self.socket.close()


class DbOps:
    def __init__(self, logger) -> None:
        self.commands = {"get_doc": self.get_doc,
                         "put_doc": self.put_doc,
                         "del_doc": self.del_doc,
                         }

    def process_message(self, message):
        cmd = json.loads(message.decode('utf-8'))
        return self.commands[cmd['action']](cmd)

    def get_doc(self, message):
        key_path = os.path.join(EFDB_PATH, message['name'])
        res = "Not found"
        if os.path.exists(key_path):
            with open(key_path, 'r') as f:
                res = f.read()
        return res

    def del_doc(self, message):
        key_path = os.path.join(EFDB_PATH, message['name'])
        if os.path.exists(key_path):
            os.remove(key_path)
            return "Deleted"
        else:
            return "Not Found"

    def put_doc(self, message):
        key_path = os.path.join(EFDB_PATH, message['name'])
        # if exist override
        with open(key_path, 'w') as f:
            f.write(message['data'])

        return "Put"


class EfdbServer:
    def __init__(self, logger, ip_address='localhost', port=9999) -> None:
        self.server_address = (ip_address, port)
        self.logger = logger

    def serve(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # to restart quickly when it terminates avoid port in use
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        self.sock.listen(NUMBER_OF_CLIENTS)

        while True:
            # waits for conn at accept() and not proceed
            newSocket, address = self.sock.accept()
            receivedData = newSocket.recv(MESSAGE_SIZE)
            if receivedData:
                handler = RequestHandler(server_log, newSocket,
                                         address, receivedData)
                handler._process()


if __name__ == '__main__':
    server = EfdbServer(server_log)
    server.serve()

import json
import os
import socket
import logging


class RequestHandler:
    """Process request/command and return result/response"""
    def __init__(self, logger, socket, address, request, db_path) -> None:
        self.request = request
        self.socket = socket
        self.address = address
        self.logger = logger
        self.db_path = db_path
        self.db_ops = DbOps(logger, self.db_path)

    def _process(self):
        self.logger.info(self.request)
        result, message = self.db_ops.process_message(self.request)
        response = '|'.join([result, message])
        # response = 'HTTP/1.0 200 OK\n\nSuccess!'
        self.socket.sendall(response.encode())
        self.socket.close()


class DbOps:
    """Performs db operations get/put/del"""
    def __init__(self, logger, db_path) -> None:
        self.db_path = db_path
        self.commands = {"get_doc": self.get_doc,
                         "put_doc": self.put_doc,
                         "del_doc": self.del_doc,
                         }

    def process_message(self, message):
        cmd = json.loads(message.decode('utf-8'))
        return self.commands[cmd['action']](cmd)

    def _get_doc_path(self, cmd):
        return os.path.join(self.db_path, cmd['path'])

    def _get_doc_full_name(self, cmd):
        doc_path = self._get_doc_path(cmd)
        doc_full_name = os.path.join(doc_path, cmd["name"])
        return doc_full_name

    def _is_doc_exist(self, path):
        return os.path.exists(path)

    def get_doc(self, cmd):
        doc_full_name = self._get_doc_full_name(cmd)
        if self._is_doc_exist(doc_full_name):
            with open(doc_full_name, 'r') as f:
                data = f.read()
            return 'OK', data
        else:
            return 'NA', 'Not Found'

    def del_doc(self, cmd):
        doc_full_name = self._get_doc_full_name(cmd)
        if self._is_doc_exist(doc_full_name):
            os.remove(doc_full_name)
            return 'OK', 'Deleted'
        else:
            return 'NA', 'Not Found'

    def put_doc(self, cmd):
        doc_path = self._get_doc_path(cmd)
        doc_full_name = self._get_doc_full_name(cmd)
        if not self._is_doc_exist(doc_path):
            os.makedirs(doc_path, exist_ok=True)
        with open(doc_full_name, 'w') as f:
            f.write(cmd['data'])
        if self._is_doc_exist(doc_full_name):
            message = 'Updated'
        else:
            message = 'Put'
        return 'OK', message


class EfdbServer:
    """
    Service to listen incoming connection
    """
    number_of_clients = 1
    message_size = 4096
    module_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(module_path, "data")
    log_path = os.path.join(module_path, "log")  # log folder
    log_file = os.path.join(log_path, 'server.log')  # log file

    def __init__(self, db_path=None, log_path=None,
                 ip_address='localhost',
                 port=9999) -> None:
        self.server_address = (ip_address, port)
        if db_path:
            self.db_path = db_path
        if log_path:
            self.log_path = log_path
        paths_to_check = [self.db_path, self.log_path, ]
        paths_to_check = list(map(self._create_path_if_not_exist,
                                  paths_to_check))
        # region logging
        logging.basicConfig(format='%(asctime)s %(message)s',
                            level=logging.INFO,
                            filename=self.log_file,
                            filemode='a')
        self.logger = logging.getLogger('server')
        self.logger.info('Server Initializing ...')
        # endregion

        self.logger.info(paths_to_check)

    def _create_path_if_not_exist(self, folder_path):
        os.makedirs(folder_path, exist_ok=True)
        return 'Checked:' + folder_path

    def serve(self) -> None:
        """start listening incoming connections"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # to restart quickly when it terminates avoid port in use
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        self.sock.listen(self.number_of_clients)

        while True:
            # waits for conn at accept() and not proceed
            newSocket, address = self.sock.accept()
            receivedData = newSocket.recv(self.message_size)
            if receivedData:
                handler = RequestHandler(self.logger, newSocket,
                                         address, receivedData, self.db_path)
                handler._process()


if __name__ == '__main__':
    server = EfdbServer()
    server.serve()

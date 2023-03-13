import os, sys

class EfdbServer:
    """
    Service to listen incoming connection
    """
    module_path = os.path.dirname(os.path.abspath(__file__))
    db_path = module_path + "/data"
    number_of_clients = 1
    message_size = 4096
    log_path = module_path + '/log'  # log folder
    log_file = log_path + '/server.log'  # log file
    
    def __init__(self, db_path=None) -> None:
        if db_path: self.db_path = db_path
        print(self.db_path)


e = EfdbServer('emre')



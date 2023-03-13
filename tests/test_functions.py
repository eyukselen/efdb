import unittest
import json
import os
import sys

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.client import Client


# with open('./data_file.json') as f:
#     json_file = json.load(f)



class TestDBOps(unittest.TestCase):

    def test_get(self):
        client = Client(ip_address='localhost', port=9999)
        res = client.send_command({"action": "get_doc", "path": "bucket1", "name": "doc1"})
        self.assertEqual(str(res), 'NA|Not Found')

    def test_put_1(self):
        client = Client(ip_address='localhost', port=9999)
        res = client.send_command({"action": "put_doc", "path": "bucket1", "name": "doc1",
                                   "data": "This is a sample data"})
        self.assertEqual(str(res), 'OK|Updated')

    def test_put_2(self):
        client = Client(ip_address='localhost', port=9999)
        res = client.send_command({"action": "put_doc", "path": "bucket1", "name": "doc0",
                                   "data": "This is a sample data"})
        self.assertEqual(str(res), 'OK|Updated')

    def test_del_1(self):
        client = Client(ip_address='localhost', port=9999)
        res = client.send_command({"action": "del_doc", "path": "bucket1", "name": "doc1"})
        self.assertEqual(str(res), 'OK|Deleted')


if __name__ == '__main__':
    unittest.main()
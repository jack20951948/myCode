import threading
import socket
import wx
from wx.lib.pubsub import pub

encoding = 'utf-8'
BUFSIZE = 1024

# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.keepAlive = 1
        self.client = client

    def run(self):
        while self.keepAlive:
            data = self.client.recv(BUFSIZE)
            if(data):
                string = bytes.decode(data, encoding)
                wx.CallAfter(pub.sendMessage, 'reload', parameters=string)
            else:
                break
        print("close:", self.client.getpeername())


    def killAlive(self):
        self.keepAlive = 0

# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class SynListener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.setDaemon(True)
        self.keepAlive = 1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(0)

    def run(self):
        print("listener started")
        while self.keepAlive:
            client, cltadd = self.sock.accept()
            self.reader = Reader(client)
            self.reader.start()
            cltadd = cltadd
            print("accept a connect")

    def killAlive(self):
        self.keepAlive = 0
        self.reader.killAlive()
        self.sock.close()

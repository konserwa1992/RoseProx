import socket
from threading import Thread

class ProxToServerGame(Thread):
    
    def __init__(self,host,port):
        super(ProxToServerGame,self).__init__()
        self.game = None
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((host,port))

    def run(self):
        while(True):
            data=self.server.recv(4096)
            if data:
                print("[S->G] "+str(self.port))
                print(' '.join(format(byte, '02X') for byte in data))
                self.game.sendall(data)


class Game2ProxyGame(Thread):
    def __init__(self,host,port):
        super(Game2ProxyGame,self).__init__()
        self.server = None
        self.port= port
        self.host = host
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((host,port))
        sock.listen(1)
        self.game, addr = sock.accept()

    def run(self):
        while(True):
            data=self.game.recv(4096)
            if data:
                print("[G->S] "+str(self.port))
                print(' '.join(format(byte, '02X') for byte in data))
                self.server.sendall(data)



class GameProxy(Thread):
    def __init__(self, from_host,to_host,port):
        super(GameProxy, self).__init__()
        self.from_host =from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while(True):
           print("Wait to connection")
           self.g2p = Game2ProxyGame(self.from_host,self.port)
           self.p2s = ProxToServerGame(self.to_host,self.port)
           print("CONNECTED")
           self.g2p.server = self.p2s.server
           self.p2s.game = self.g2p.game

           self.g2p.start()
           self.p2s.start()


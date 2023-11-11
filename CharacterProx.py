import socket
from threading import Thread

class ProxToServerCharacterSelect(Thread):
    
    def __init__(self,host,port):
        super(ProxToServerCharacterSelect,self).__init__()
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
                self.game.sendall(ChangeIPPacket(data))


class Game2ProxyCharacterSelect(Thread):
    def __init__(self,host,port):
        super(Game2ProxyCharacterSelect,self).__init__()
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
                self.server.sendall(ChangeIPPacket(data))

def ChangeIPPacket(packet):
    originalIpSequence = bytes.fromhex("34352E37372E3232312E323332")

    if originalIpSequence not in packet:
        print("Wzór nie został znaleziony w pakiecie.")
        return packet

    newIPsequence = bytes.fromhex("3132372E302E302E31")
    packet = packet.replace(originalIpSequence, newIPsequence)

    #New packet sizes
    packet = packet.replace(bytes.fromhex("1e00"), bytes.fromhex("1a00"), 1)

    return packet

class ProxyCharacter(Thread):
    def __init__(self, from_host,to_host,port):
        super(ProxyCharacter, self).__init__()
        self.from_host =from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while(True):
           print("Wait to connection")
           self.g2p = Game2ProxyCharacterSelect(self.from_host,self.port)
           self.p2s = ProxToServerCharacterSelect(self.to_host,self.port)
           print("CONNECTED")
           self.g2p.server = self.p2s.server
           self.p2s.game = self.g2p.game

           self.g2p.start()
           self.p2s.start()


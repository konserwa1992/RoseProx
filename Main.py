from LoginProx import ProxyLogin
from CharacterProx import ProxyCharacter
from GameProxy import GameProxy

master_prox = ProxyLogin("127.0.0.1","45.77.221.232",29000)
master_prox.start()

master_prox = ProxyCharacter("127.0.0.1","45.77.221.232",20470)
master_prox.start()

master_prox = GameProxy("127.0.0.1","45.77.221.232",20471)
master_prox.start()
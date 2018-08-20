import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from card import Card

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

cost = {"black": 1,
        "red": 1,
        "green": 0,
        "blue": 0,
        "white": 0}
gem_count = {"black": 1,
        "red": 0,
        "green": 0,
        "blue": 0,
        "white": 0,
        "gold": 0}
c = [cost, gem_count, 0, False, 1, [100, 100]]


class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################
    
    def Network_message(self, data):
        if data['message'] == "gg ez":
            data['message'] = 'OMEGALUL'

        if data['message'] == 'card':
            self._server.SendToAll({"action": "table", "table": c})
        else:
            self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})
    def Network_nickname(self, data):
        self.nickname = data['nickname']
        self._server.SendPlayers()

class ChatServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print('Server launched')
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
    def AddPlayer(self, player):
        print("New Player" + str(player.addr))
        self.players[player] = True
        self.SendPlayers()
        print("players", [p for p in self.players])
    
    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        del self.players[player]
        self.SendPlayers()
    
    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    s = ChatServer(localaddr=(host, int(port)))
    s.Launch()

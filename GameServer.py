import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from SplendorClasses import *
from game import Game

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


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
            data['message'] = 'Mommy says that people my age shouldn\'t suck their thumbs.'

    def Network_nickname(self, data):
        self.nickname = data['nickname']
        self._server.SendPlayers()

class GameServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = {}
        print('Server launched')
        self.games = []
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
    def AddPlayer(self, player):
        print("New Player" + str(player.addr))
        self.players[player] = Player(player.addr)
        self.SendPlayers()
        print("players", [p for p in self.players])
        if len(self.players) == 1:
            self.games += [Game(self.players[player])]

    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        del self.players[player]
        self.SendPlayers()
    
    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def SendTable_Cards(self, data):
        self.SendToAll({"action": "table_cards", "table_cards": [g.get_cards_shown()[playerID] for playerID in self.players.keys()]})
    '''
    def SendTable_Tokens(self, data):
        self.SendToAll({"action": "table_tokens", "table_tokens": [g.get_tokens_shown()[playerID] for playerID in self.players.keys()]})
    '''
    
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
    s = GameServer(localaddr=(host, int(port)))
    s.Launch()


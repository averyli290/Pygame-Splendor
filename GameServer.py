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
        self._server.SendToAll({"action":"message","message":data['message'],"who":self.nickname})
        self._server.SendTable_Cards()

    def Network_nickname(self, data):
        # Sets nickname
        self.nickname = data['nickname']
        self._server.SendPlayers()


class GameServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary() 
        print('Server launched')
        self.games = []
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
        if len(self.players) == 2:
            self.games += [Game([self.players[p] for p in self.players])]
    
    def AddPlayer(self, player):
        # Adds player to dict and sends the player's address back to them for use of playerID
        print("New Player" + str(player.addr))
        self.players[player] = player.addr
        self.SendPlayers()
        self.SendToPlayer({"action": "player_addr", "player_addr": player.addr}, player)

    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        del self.players[player]
        self.SendPlayers()
    
    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})

    def SendToPlayer(self, data, player):
        player.Send(data)
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def SendTable_Cards(self):
        print(self.games[0].get_cards().keys())
        if len(self.games) > 0:
            self.SendToAll({"action": "table_cards", "table_cards": self.games[0].get_cards()})
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


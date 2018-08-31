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
        elif data['message'] == 'startGame()':
            self._server.StartGame()

        self._server.SendToAll({"action":"message","message":data['message'],"who":self.nickname})

    def Network_nickname(self, data):
        # Sets nickname
        self.nickname = data['nickname']
        self._server.SendPlayers()

    def Network_mouseclick(self, data):
        # Sends the mouse data over to the server
        self._server.HandleMouse(data['mouseclick'])


class GameServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary() 
        print('Server launched')
        self.games = []
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
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
        ## FIX GAMES[0] PART TO ALLOW FOR MULTIPLE GAMES
        if len(self.games) > 0:
            self.SendToAll({"action": "table_cards", "table_cards": self.games[0].get_cards()})
    
    def SendTable_Tokens(self):
        if len(self.games) > 0:
            self.SendToAll({"action": "table_tokens", "table_tokens": self.games[0].get_tokens()})

    def HandleMouse(self, data):
        # Handles Mouse data being sent
        pass

    def StartGame(self):
        self.games += [Game([self.players[p] for p in self.players])]

        ## Test code
        a = self.games[0]
        Player1 = a.turn_list[0]
        t1 = Token("blue", 1)
        t2 = Token("red", 1)
        t3 = Token("green", 1)
        t4 = Token("white", 1)
        t5 = Token("black", 1)
        tc1 = TokenCache([t1, t2, t3])
        tc2 = TokenCache([t4, t5, t1])
        tc3 = TokenCache([t2, t3, t4])
        turns = [tc1, tc2, tc3]
        for i in range(3):
            good = a.handle_turn("tokenDraw", [turns[i]])
            if a.get_turn() != Player1:
                for j in range(3):
                    a.next_turn()
            for player in a.players:
                print(a.players[player].get_tokens().get_total_num(), player, a.get_turn())
        t1 = Token("blue", 2)
        t2 = Token("red", 2)
        t3 = Token("green", 2)
        t4 = Token("white", 2)
        t6 = Token("gold", 1)
        tc4 = TokenCache([t1, t2, t3, t4, t5, t6])
        tc5 = TokenCache([t6])

        print(a.handle_turn("reserveCard", [1, 0]))
        print(a.players[Player1].get_reservedCards())
        for player in a.players:
            print(a.players[player].get_tokens().get_total_num(), player, a.get_turn())

        if a.get_turn() != Player1:
            for j in range(3):
                a.next_turn()

        print(a.handle_turn("reserveCard", [1, 0]))
        print(a.players[Player1].get_reservedCards())
        for player in a.players:
            print(a.players[player].get_tokens().get_total_num(), player, a.get_turn())

        print(a.handle_turn("returnTokens", [tc5]))

        if a.get_turn() != Player1:
            for j in range(3):
                a.next_turn()

        print(a.players[Player1].get_reservedCards()[0].get_cost())
        print(a.handle_turn("buyReserveCard", [0, tc4]))
        print(a.players[Player1].get_cards().get_cache())
        print(a.players[Player1].get_reservedCards())

        print(a.table.get_cardsShown()[1][0].get_cost())
        print(a.handle_turn("buyTableCard", [1, 0, tc4]))
        print(a.players[Player1].get_cards().get_cache())

        if a.get_turn() != Player1:
            for j in range(3):
                a.next_turn()

        print(a.table.get_cardsShown()[1][0].get_cost())
        print(a.handle_turn("buyTableCard", [1, 0, TokenCache()]))
        print(a.players[Player1].get_cards().get_cache())

    def Launch(self):
        while True:
            if len(self.games) > 0:
                self.SendTable_Cards()
                self.SendTable_Tokens()
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


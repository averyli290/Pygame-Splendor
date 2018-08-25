import pygame
from general_functions import *
from random import shuffle
from SplendorClasses import *

class Game:

    gemColors = ["black", "red", "green", "blue", "white", "gold"]

    def create_table_from_file(self, filename):
        decks = {}
        with open(filename, ('r')) as f:
            line = f.readline().split(' ')
            while line != [""]:
                # color(s) (for gem_count), category, deckID, points, "black", "red", "green", "blue", "white"
                gemColors = ["black", "red", "green", "blue", "white", "gold"]
                gem_count = {color: 0 for color in gemColors}
                gem_count[line[0]] += 1
                category = int(line[1])
                deckID = int(line[2])
                points = int(line[3])
                parent_surface = None
                cost = {"black": int(line[4]),
                        "red": int(line[5]),
                        "green": int(line[6]),
                        "blue": int(line[7]),
                        "white": int(line[8])}
                card = Card(cost, gem_count, points, False, category, parent_surface)
                if deckID not in decks.keys():
                    decks[deckID] = []
                decks[deckID].append(card)
                line = f.readline().split(' ')
        for ID in decks.keys():
            shuffle(decks[ID])
        decks_actual = []
        for ID in decks.keys():
            deck_actual = Deck(decks[ID], decks[ID][0].get_category(), 4, ID)
            decks_actual.append(deck_actual)
        return Table(decks_actual)

    def __init__(self, playerIDs, decks = "cards.txt"):
        # creates a new game given supply decks and player IDs
        if type(decks) == type("a generic string"):
            self.table = self.create_table_from_file(decks)
        else:
            self.table = Table(decks)
        self.players = {}
        for ID in playerIDs:
            self.players[ID] = Player(ID)
        self.turn_list = playerIDs
        self.turn_index = 0
        self.tokenBank = TokenCache([Token(color, 7) for color in self.gemColors])
        self.finalStage = [0 for player in playerIDs]
        self.tokenLimitExceeded = False

    def get_turn(self):
        # Gets whose turn it is
        return self.turn_list[self.turn_index]

    def convert_card(self, card):
        # Converts given card into a list of parameters
        return [card.cost, card.gem_count, card.points, card.one_use_only, card.category, card.coords, card.width, card.height]
    
    def get_cards(self):
        # Returns all of the cards to be displayed on the screen for each player
        # Send tuple with data and coords depending on player
        #return_me = {(playerID, []) for playerID in self.players.keys()}
        list_of_cards = []
        supplyDecks = self.table.get_supplyDecks()
        i = 0
        for deckID in supplyDecks:
            list_of_cards.append(({"black": supplyDecks[deckID].get_category(),
                                    "red":0,
                                    "green":0,
                                    "blue":0,
                                    "white":0},
                             {"black": 0,
                                    "red":0,
                                    "green":0,
                                    "blue":0,
                                    "white":0,
                                    "gold":0},
                             0,False,supplyDecks[deckID].get_category(),[405,205+170*i],106,150))
            for j in range(len(self.table.get_cardsShown()[deckID])):
                card = self.table.get_cardsShown()[deckID][j]
                new_card = self.convert_card(card)
                new_card[5] = [405+(j+1)*131, 205+170*i]
                list_of_cards.append(tuple(new_card))
            i += 1
        return_me={}
        for p in self.players:
            return_me[p] = list_of_cards
            playerCardCache = self.players[p].get_cards().get_cache()
            for i in range(len(self.gemColors)):
                color = self.gemColors[i]
                for j in range(len(playerCardCache[color])):
                    card = playerCardCache[color][j]
                    new_card = self.convert_card(card)
                    new_card[5] = [405+i*131, 715+35*j]
                    return_me[p].append(tuple(new_card))
        return return_me

    def convert_token(self, token):
        # Converts given token into a list of parameters
        return [token.gemColor, token.num, token.coords, token.radius]
    
    def get_tokens(self):
        # Returns all of the tokens to be displayed on the screen for each player
        # Send tuple with data and coords depending on player
        return_me={}
        for p in self.players:
            return_me[p] = [("blue", 3, [100, 100], 40)]
        return return_me 

    def clickSelection(self, coords, player):
        # Given the position of a click by a player, find the card/token selected
        x = coords[0]
        y = coords[1]
        if 405 <= x <= 1440-405 and 205 <= y <= 900-205: # table
            deck_index = -1
            for i in range(3):
                if 205+170*i <= y <= 205+170*i+150:
                    deck_index = i
            card_index = -1
            for i in range(4):
                if 405+(i+1)*131 <= x <= 405+(i+1)*131+106:
                    card_index = j
            if deck_index > 0 and card_index > 0:
                return ["TableCard", deck_index, card_index]
        if 405 <= x <= 1440 and 715 <= y: # player's cards (will we need this?)
            gem_index = -1
            card_index = -1
            for i in range(len(self.gemColors)):
                playerCardCache = self.players[player].get_cards().get_cache()
                color = self.gemColors[i]
                if 405+i*131 <= x <= 405+i*131+106:
                    gem_index = i
                for j in range(len(playerCardCache[color])):
                    if 715+35*j <= y <= 715+35*j+106:
                        card_index = j
            if gem_index != -1 and card_index != 1:
                return ["PlayerCard", self.gemColors[gem_index], card_index]
        return ["None"]

    def isTokenLimitExceeded(self):
        # Gets the tokenLimitExceeded variable
        return self.tokenLimitExceeded

    def get_finalStage(self):
        # Gets the state of the final stage of the game ([0,0,...,0] for "is not in final stage")
        return self.finalStage

    def isOver(self):
        # Determines whether the game is over
        return self.finalStage[self.turn_index] == 1

    def next_turn(self):
        # Goes to the next player's turn
        if self.players[self.get_turn()].get_points() >= 15 or sum(self.finalStage) > 0:
            self.finalStage[self.turn_index] = 1
        self.turn_index = (self.turn_index + 1) % len(self.turn_list)

    def canAfford(self, player, cost, gems_spent = TokenCache()):
        # Determines whether the player's cards and the gems spent cover the cost (of a card)
        # Does not yet detect whether it's exactly enough tokens, so good luck if you overspend... [FIX (it's an easy one)]
        gemColors = ["black", "red", "green", "blue", "white", "gold"]
        total_gems = player.get_cards().get_gems()
        print("total_gems:", total_gems.get_total_num())
        total_gems.receive(gems_spent)
        total_deficit = 0
        for color in gemColors[:5]:
            total_deficit += max(0, cost.get_num(color) - total_gems.get_num(color))
            print("marker:", cost.get_num(color), total_gems.get_num(color))
        return total_deficit <= total_gems.get_num("gold")

    def turn_tokenDraw(self, tokens):
        # Player uses turn to gain tokens from bank (tokens is a TokenCache object)
        # Returns 1 (true) if successful, 0 (false) if not, and will not do if false
        # Returns 2 if token limit is exceeded
        player = self.players[self.get_turn()]
        gemColors = ["black", "red", "green", "blue", "white", "gold"]
        if tokens.get_num("gold") > 0:
            return False
        distribution = sorted([tokens.get_num(color) for color in gemColors])
        greatestGem = ""
        for color in gemColors:
            if tokens.get_num(color) == distribution[-1]:
                greatestGem = color
        if not (distribution == [0,0,0,1,1,1] or (distribution == [0,0,0,0,0,2] and self.tokenBank.get_num(greatestGem) >= 4)):
            return False
        if not self.tokenBank.give(tokens):
            return False
        return 2 - (player.gainTokens(tokens))

    def turn_buyTableCard(self, deckID, index, tokens):
        # Player uses turn to buy a card from among the shown cards (tokens is a TokenCache object)
        # Returns true if successful, false if not, and will not do if false
        player = self.players[self.get_turn()]
        gemColors = ["black", "red", "green", "blue", "white", "gold"]
        card = self.table.get_cardsShown()[deckID][index]
        cost_dict = card.get_cost()
        cost = TokenCache([Token(color, cost_dict[color]) for color in gemColors[:5]])
        if not self.canAfford(player, cost, tokens):
            return False
        if not player.giveTokens(tokens):
            return False
        self.tokenBank.receive(tokens)
        player.gainCard(self.table.pick_card(deckID, index))
        return True

    def turn_buyReserveCard(self, index, tokens):
        # Player uses turn to buy a card in reserve (tokens is a TokenCache object)
        # Returns true if successful, false if not, and will not do if false
        player = self.players[self.get_turn()]
        gemColors = ["black", "red", "green", "blue", "white", "gold"]
        card = player.get_reservedCards()[index]
        cost_dict = card.get_cost()
        cost = TokenCache([Token(color, cost_dict[color]) for color in gemColors[:5]])
        if not self.canAfford(player, cost, tokens):
            return False
        if not player.giveTokens(tokens):
            return False
        self.tokenBank.receive(tokens)
        player.gainCard(player.pickReserveCard(index))
        return True

    def turn_reserveCard(self, deckID, index):
        # Player uses turn to buy a card in reserve (tokens is a TokenCache object)
        # Returns 1 (true) if successful, 0 (false) if not, and will not do if false
        # Returns 2 if token limit is exceeded
        player = self.players[self.get_turn()]
        if not player.canReserveCard():
            return False
        card = self.table.pick_card(deckID, index)
        player.reserveCard(card)
        good = 1
        if self.tokenBank.get_num("gold") > 0:
            goldToken = Token("gold", 1)
            goldTokenCache = TokenCache([goldToken])
            good = 2 - (player.gainTokens(goldTokenCache))
        return good
            
    def turn_returnTokens(self, tokens):
        # Player returns some tokens to the bank (tokens is a TokenCache object)
        # Returns true if successful, false if not, and will not do if false
        player = self.players[self.get_turn()]
        if player.get_tokens().get_total_num() - tokens.get_total_num() != player.get_tokens().get_limit():
            return False
        if not player.giveTokens(tokens):
            return False
        self.tokenBank.receive(tokens)
        return True

    def handle_turn(self, turn_type, parameters):
        # Handles a player's turn using the "turn" functions
        # Does not use the turn if such function returns false
        # Returns true if turn is complete, false if unsuccessful or if player is to return tokens
        if self.tokenLimitExceeded and turn_type == "returnTokens": # fixed
            good = self.turn_returnTokens(parameters[0])
        elif turn_type == "tokenDraw": # fixed
            good = self.turn_tokenDraw(parameters[0])
        elif turn_type == "buyTableCard": # fixed
            good = self.turn_buyTableCard(parameters[0], parameters[1], parameters[2])
        elif turn_type == "buyReserveCard": # fixed
            good = self.turn_buyReserveCard(parameters[0], parameters[1])
        elif turn_type == "reserveCard": # fixed
            good = self.turn_reserveCard(parameters[0], parameters[1])
        if good == 2:
            self.tokenLimitExceeded = True
            good = False
        if good:
            self.tokenLimitExceeded = False
            self.next_turn()
        return good

########################################
## Test code for conceptual operation ##
########################################

a = Game(['Player1', 'Player2', 'Player3', 'Player4'])
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
    if a.get_turn() != "Player1":
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
print(a.players["Player1"].get_reservedCards())
for player in a.players:
    print(a.players[player].get_tokens().get_total_num(), player, a.get_turn())

if a.get_turn() != "Player1":
    for j in range(3):
        a.next_turn()

print(a.handle_turn("reserveCard", [1, 0]))
print(a.players["Player1"].get_reservedCards())
for player in a.players:
    print(a.players[player].get_tokens().get_total_num(), player, a.get_turn())

print(a.handle_turn("returnTokens", [tc5]))

if a.get_turn() != "Player1":
    for j in range(3):
        a.next_turn()

print(a.players["Player1"].get_reservedCards()[0].get_cost())
print(a.handle_turn("buyReserveCard", [0, tc4]))
print(a.players["Player1"].get_cards().get_cache())
print(a.players["Player1"].get_reservedCards())

"""
print(a.table.get_cardsShown()[1][0].get_cost())
print(a.handle_turn("buyTableCard", [1, 0, tc4]))
print(a.players["Player1"].get_cards().get_cache())

if a.get_turn() != "Player1":
    for j in range(3):
        a.next_turn()

print(a.table.get_cardsShown()[1][0].get_cost())
print(a.handle_turn("buyTableCard", [1, 0, TokenCache()]))
print(a.players["Player1"].get_cards().get_cache())
"""

import pygame
from general_functions import *
from random import shuffle
from SplendorClasses import *

class Game:

    gemColors = ["black", "red", "green", "blue", "white", "gold"]

    def create_table_from_file(self, filename):
        decks = {}
        with open(filename, ('r')) as f:
            line = f.readline().split(',')
            line[0] = eval(line[0])
            line[-1] = line[-1][0]
            print(line)
            # color(s) (for gem_count), category, deckID, points, "black", "red", "green", "blue", "white"
            gemColors = ["black", "red", "green", "blue", "white", "gold"]
            gem_count = {}
            for color in get_colors():
                gem_count[color] = 0
            gem_count[line[0]] += 1
            category = int(line[1])
            deckID = int(line[2])
            points = int(line[3])
            cost = {"black": int(line[4]),
                    "red": int(line[5]),
                    "green": int(line[6]),
                    "blue": int(line[7]),
                    "white": int(line[8])}
            card = Card(parent_surface, cost, gem_count, points, False, category)
            if deckID not in decks:
                decks[deckID] = []
            decks[deckID].append(card)
        for ID in decks:
            shuffle(decks[ID])
        return Table(decks.values())

    def __init__(self, playerIDs, decks = "cards.txt"):
        # creates a new game given supply decks and player IDs
        if type(decks) == type("a generic string"):
            self.table = self.create_table_from_file(decks)
        else:
            self.table = Table(decks)
        self.players = {}
        for ID in playerIDs:
            self.players[ID] = Player(ID, 10)
        self.turn_list = playerIDs
        self.turn_index = 0
        self.tokenBank = TokenCache([Token(color), 7])
        self.finalStage = [0 for player in self.playerIDs]
        self.tokenLimitExceeded = False

    def get_turn(self):
        # Gets whose turn it is
        return self.turn_list[self.turn_index]
    
    def get_cards_shown(self):
        # Returns all of the positions of the cards to be displayed on the screen for each player

        to_display = {(playerID,[]) for playerID in self.player.keys()}
        for playerID in to_display:
            for c in self.table.get_cardsShown():
                info = (None,c.get_cost(),c.get_gem_count(),c.get_points(),c.get_category(),c.get_size()[0],c.get_size()[1])
                to_display[playerID].append(info)
            
        return None

    def isTokenLimitExceeded(self):
        # Gets the tokenLimitExceeded variable
        return self.tokenLimitExceeded

    def get_finalStage(self):
        # Gets the state of the final stage of the game ([0,0,0,0] for "is not in final stage")
        return self.finalStage

    def isOver(self):
        # Determines whether the game is over
        return self.finalStage[self.turn_index] == 1

    def next_turn(self):
        # Goes to the next player's turn
        if self.players[self.get_turn()].get_points() >= 15 or sum(self.finalStage) > 0:
            self.finalStage[self.turn_index] = 1
        self.turn_index = (self.turn_index + 1) % len(self.turn_list)

    def canAfford(player, cost, gems_spent = TokenCache()):
        # Determines whether the player's cards and the gems spent cover the cost (of a card)
        total_gems = TokenCache()
        gemColors = ["black", "red", "green", "blue", "white", "gold"]
        for color in gemColors:
            total_gems.receive(player.get_tokens())
            total_gems.receive(gems_spent())
        total_deficit = 0
        for color in gemColors[:5]:
            total_deficit += max(0, cost.get_num(color) - total_gems.get_num(color))
        return total_deficit <= total_gems.get_num("gold")

    def turn_tokenDraw(self, tokens):
        # Player uses turn to gain tokens from bank (tokens is a TokenCache object)
        # Returns 1 (true) if successful, 0 (false) if not, and will not do if false
        # Returns 2 if token limit is exceeded
        player = self.players[self.get_turn()]
        gemColors = ["black", "red", "green", "blue", "white", "gold"]
        if self.tokens.get_num("gold") > 0:
            return False
        distribution = sorted([self.tokens.get_num(color) for color in gemColors])
        greatestGem = ""
        for color in gemColors:
            if self.tokens.get_num(color) == distribution[-1]:
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
        if not canAfford(player, cost, tokens):
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
        card = player.get_reservedCards[index]
        cost_dict = card.get_cost()
        cost = TokenCache([Token(color, cost_dict[color]) for color in gemColors[:5]])
        if not canAfford(player, cost, tokens):
            return False
        if not player.giveTokens(tokens):
            return False
        self.tokenBank.receive(tokens)
        player.gainCard(player.pickReservedCard(index))
        return True

    def turn_reserveCard(self, deckID, index):
        # Player uses turn to buy a card in reserve (tokens is a TokenCache object)
        # Returns 1 (true) if successful, 0 (false) if not, and will not do if false
        # Returns 2 if token limit is exceeded
        player = self.players[self.get_turn()]
        if not player.canReserveCard():
            return False
        card = self.table.pick_card(deckID, index)
        player.gainCard(card)
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
        if self.player.get_tokens().get_total_num() - tokens.get_total_num() != player.get_tokens().get_limit():
            return False
        if not self.player.give(tokens):
            return False
        self.tokenBank.receive(tokens)
        return True

    def handle_turn(self, turn_type, parameters):
        # Handles a player's turn using the "turn" functions
        # Does not use the turn if such function returns false
        # Returns true if turn is complete, false if unsuccessful or if player is to return tokens
        if self.tokenLimitExceeded:
            good = self.turn_returnTokens(parameters[0])
        if turn_type == "tokenDraw":
            good = self.turn_tokenDraw(parameters[0])
        if turn_type == "buyTableCard":
            good = self.turn_buyTableCard(parameters[0], parameters[1], parameters[2])
        if turn_type == "buyReserveCard":
            good = self.turn_buyReserveCard(parameters[0], parameters[1])
        if turn_type == "reserveCard":
            good = self.turn_reserveCard(parameters[0], parameters[1])
        if good == 2:
            self.tokenLimitExceeded = True
            good = False
        if good:
            self.tokenLimitExceeded = False
            self.next_turn()
        return good


a = Game([12345])

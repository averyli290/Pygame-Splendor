import pygame
from general_functions import *
from random import shuffle
from SplendorClasses import *

class Game:

    def create_table_from_file(self, filename):
        decks = {}
        with open(filename, ('r')) as f:
            line = f.readline().split(',')
            # color(s) (for gem_count), category, deckID, points, "black", "red", "green", "blue", "white"
            gemColors = ["black", "red", "green", "blue", "white", "gold"]
            gem_count = {color: 0 for color in gemColors}
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
            if deckID not in decks.keys():
                decks[deckID] = []
            decks[deckID].append(card)
        for ID in decks.keys():
            shuffle(decks[ID])
        return Table(decks.values())

    def __init__(self, playerIDs, decks = "cards.txt"):
        # creates a new game given supply decks and player IDs
        if type(decks) == type("a generic string"):
            self.table = create_table_from_file(decks)
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
    
    def get_card_coords(self):
        # Returns all of the positions of the cards to be displayed on the screen for each player
        return None

    def isTokenLimitExceeded(self):
        # Gets the tokenLimitExceeded variable
        return self.tokenLimitExceeded

    def get_finalStage(self):
        # Gets the state of the final stage of the game ([0,0,0,0] for "is not in final stage")
        return self.finalStage

    def isOver(self):
        # Determines whether the game is over
        return self.finalStage == [1,1,1,1]

    def next_turn(self):
        # Goes to the next player's turn
        if self.players[self.get_turn()].get_points() >= 15 or sum(self.finalStage) > 0:
            self.finalStage[self.turn_index] = 1
        self.turn_index = (self.turn_index + 1) % len(self.turn_list)

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
        if not self.tokenBank.give():
            return False
        return 2 - (player.gainTokens(tokens))

    def turn_buyTableCard(self, deckID, index, tokens):
        # Player uses turn to buy a card from among the shown cards (tokens is a TokenCache object)
        # Returns true if successful, false if not, and will not do if false
        pass

    def turn_buyReserveCard(self, index, tokens):
        # Player uses turn to buy a card in reserve (tokens is a TokenCache object)
        # Returns true if successful, false if not, and will not do if false
        pass

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
        pass

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

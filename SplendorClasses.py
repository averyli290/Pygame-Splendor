import pygame

class Deck:

	def __init__(self, cards = [], category=0, numCardsShown=4, deckID=None):
		# initializes variables

		self.cards = cards
		self.category = category
		self.deckID = deckID
		self.numCardsShown = numCardsShown

	def draw_card(self):
		# removes "top card of deck" and returns it
		if len(self.cards) == 0:
			return None
		return self.cards.pop()

	def get_deckID(self):
		# returns deck ID
		return self.deckID

	def get_numCardsShown(self):
		# returns the number of cards which are to be dealt out on the table
		return self.numCardsShown

	def get_category(self):
		# returns the category of the cards (should be the same)
		return self.category

	def get_numCards(self):
		# returns the number of cards in the deck
		return len(self.cards)

class Table:
	cardsShown = {}
	supplyDecks = {}

	def __init__(self, decks):
		# initializes and sets up the table given decks
		for deck in decks:
			supplyDecks[deck.deckID] = decks
			cardsShown[deck.deckID] = []
		for deckID in supplyDecks.keys():
			for i in range(supplyDecks[deckID].get_numCardsShown()):
				if supplyDecks[deckID].get_numCards() > 0:
					cardsShown[deckID].append(supplyDecks[deckID].draw_card())

	def pick_card(self, deckID, index):
		# removes a card shown, replaces it with the top card of its corresponding deck,
		# and returns the removed card
		pickedCard = cardsShown[deckID].pop(index)
		if supplyDecks[deckID].get_numCards() > 0:
			cardsShown[deckID].insert(index, supplyDecks[deckID].draw_card())
		return pickedCard

class Token:

	def __init__(self, gemColor, num=0):
		# initializes variables
		self.gemColor = gemColor
		self.num = num

	def get_num(self):
		# gets the number of tokens
		return self.num

	def get_gemColor(self):
		# gets the gem color
		return self.gemColor

	def increase(self, increment):
		# increases token count
		self.num += increment

	def decrease(self, decrement):
		# decreases token count
		self.num -= decrement

class TokenCache:
	cache = {}

	def __init__(self, listOfTokens = [], limit = 10):
		# initializes the cache from the list of tokens (assuming no two have the same color)
		gemColors = ["black", "red", "green", "blue", "white", "gold"]
		for color in gemColors:
			self.cache[color] = Token(color)
		for token in listOfTokens:
			self.cache[token.get_gemColor] = token
		self.limit = limit

	def get_num(self, color):
		# gets the number of tokens of a color
		return self.cache[color]

	def get_total_num(self):
		# gets the total number of tokens
		return sum([self.cache[color] for color in self.cache.keys()])

	def receive(self, increment):
		# attempts to increase token count, where increment is a TokenCache
		# returns True if successful ("increment" should not be used again)
		# returns False if token limit is reached (usually meaning the player has to get rid of some tokens)
		for color in increment.keys():
			self.cache[color] += increment.get_num(color)
		return self.get_total_num() <= limit

	def give(self, decrement):
		# attempts to decrease token count, where decrement is a TokenCache
		# returns True if successful ("decrement" is now a carrier)
		# returns False if not enough tokens; the giving does not happen
		for color in decrement.keys():
			if self.cache[color] < decrement.get_num(color):
				return False
		for color in decrement.keys():
			self.cache[color] -= decrement.get_num(color):
		return True


import pygame
from general_functions import *
from random import shuffle

# From card.py

pygame.font.init()
pygame.init()

class Card:
    
    colors = get_colors()
    default_width, default_height = 70, 100   #  106, 150

    def __init__(self, cost, gem_count, points=0, one_use_only=False, category=0, parent_surface=None, coords=[0,0], width=default_width, height=default_height):
        # Sets up all of the variable needed for the card 
        # Creating the surface for the card

        self.cost = {"black": 0,
            "red": 0,
            "green": 0,
            "blue": 0,
            "white": 0}
        self.gem_count = {"black": 0,
            "red": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "gold": 0}

        self.default_font_size0 = 15 ; self.default_font_size1 = 25 # Two font sizes for the cards; self.default_font_size0 was 20
        self.default_font_size2 = 35 # Font size for the points

        self.parent_surface = parent_surface
        for gem in cost: self.cost[gem] += cost[gem]
        for gem in gem_count: self.gem_count[gem] += gem_count[gem]
        self.points = points 
        self.one_use_only = one_use_only
        self.category = category
        self.width = width
        self.height = height 
        self.coords = coords

        self.font_size0 = int(height*self.default_font_size0/self.default_height)
        self.font_size1 = int(height*self.default_font_size1/self.default_height)
        self.font_size2 = int(height*self.default_font_size1/self.default_height)
       
        self.surface = pygame.Surface((width,height)) 
        self.cardcolor = (200,200,200)
        self.surface.fill(self.cardcolor)
        
    def draw(self):
        # Draws the card onto the parent surface with cost and type 

        drawx = 0; drawy = self.surface.get_height()
        textcolor = (200,200,200); font = pygame.font.get_default_font(); italic = True; rotation=0

        textwidth = 100
        textheight = 100
        for i in range(1, 10):
            TextSurf, TextRect = display_text(str(i),self.font_size0,font,textcolor,italic,rotation)
            tw, th = TextSurf.get_size()
            textwidth = min(textwidth, tw)
            textheight = min(textheight, th)

        counter = 0
        for color in self.cost:
            if self.cost[color] > 0:
                TextSurf, TextRect = display_text(str(self.cost[color]),self.font_size0,font,textcolor,italic,rotation)
                # textwidth, textheight = TextSurf.get_size()
                drawx = int(textwidth)
                drawy -= int(textheight*1.7)
                if counter > 1:
                    drawx += int(textwidth*2.5)
                if counter % 2 == 0 and counter > 0:
                    drawy += 2*int(textheight*1.7)
                pygame.draw.circle(self.surface,(255,255,255),(drawx+textwidth//2,drawy+textheight//2),textwidth)
                pygame.draw.circle(self.surface,self.colors[color],(drawx+textwidth//2,drawy+textheight//2),int(textwidth*0.99))
                self.surface.blit(TextSurf,(drawx, drawy))
                counter += 1
        
        drawx = int(self.surface.get_width()*1.05); drawy = 0
        radius = self.surface.get_width()//5
        for color in self.gem_count:
             if self.gem_count[color] > 0:
                for i in range(self.gem_count[color]):
                    TextSurf, TextRect = display_text(str(self.cost[color]),self.font_size1,font,self.colors[color],False,rotation)
                    textwidth, textheight = TextSurf.get_size()
                    drawx -= int(textwidth*2)
                    drawy = int(textheight)//10
                    pygame.draw.circle(self.surface,(255,255,255),(drawx+textwidth//2,drawy+textheight//2),radius)
                    pygame.draw.circle(self.surface,self.colors[color],(drawx+textwidth//2,drawy+textheight//2),int(radius*0.99))
                    self.surface.blit(TextSurf,(drawx, drawy))
        if self.points > 0:
            TextSurf, TextRect = display_text(str(self.points),self.font_size2,font,self.colors["black"],italic,rotation)
            textwidth, textheight = TextSurf.get_size()
            drawx = 2*int(textwidth)//3
            drawy = int(textheight)//3
            self.surface.blit(TextSurf,(drawx, drawy))
        
        self.parent_surface.blit(self.surface, self.coords)

    def set_coords(self, new_coords):
        # Sets the coords variable to the specified coordinates
        self.coords[0], self.coords[1] = new_coords[0], new_coords[1]

    # Getters
    def get_cost(self):
        return self.cost

    def get_gem_count(self):
        return self.gem_count

    def get_points(self):
        return self.points

    def get_category(self):
        return self.category

    # isClicked
    def isClicked(self, coords):
        pass

    
# end of card.py

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

    def __init__(self, decks):
        self.cardsShown = {}
        self.supplyDecks = {}
        # initializes and sets up the table given decks
        for deck in decks:
            self.supplyDecks[deck.deckID] = deck
            self.cardsShown[deck.deckID] = []
        for deckID in self.supplyDecks.keys():
            for i in range(self.supplyDecks[deckID].get_numCardsShown()):
                if self.supplyDecks[deckID].get_numCards() > 0:
                    self.cardsShown[deckID].append(self.supplyDecks[deckID].draw_card())

    def pick_card(self, deckID, index):
        # removes a card shown, replaces it with the top card of its corresponding deck,
        # and returns the removed card
        pickedCard = self.cardsShown[deckID].pop(index)
        if self.supplyDecks[deckID].get_numCards() > 0:
            self.cardsShown[deckID].insert(index, self.supplyDecks[deckID].draw_card())
        return pickedCard

    def get_cardsShown(self):
        # gets the cards shown
        return self.cardsShown

    def get_supplyDecks(self):
        # gets the supply decks
        return self.supplyDecks

class Token:

    default_font_size = 35
    color_dict = get_colors()
    
    def __init__(self, gemColor, num=0, parent_surface=None, coords=[0,0], radius=40):
        # initializes variables
        self.gemColor = gemColor
        self.num = num
        self.radius = radius
        self.font_size = int(self.default_font_size*radius/40)
        self.parent_surface = parent_surface
        self.surface = pygame.Surface((radius*2, radius*2))
        self.surface.set_colorkey((255,0,255))
        self.coords = coords

    def draw(self, rotation = 0):
        # Draws the token on to the parent surface
        self.surface.fill((255,0,255))
        pygame.draw.circle(self.surface, (128,128,128), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.surface, self.color_dict[self.gemColor], (self.radius, self.radius), int(self.radius*0.95))
        text = str(self.num); font_size = self.font_size; font = pygame.font.get_default_font(); color = (255,255,255)
        italic = False
        TextSurf, TextRect= display_text(text, font_size, font, color, italic, rotation)
        self.surface.blit(TextSurf, ((self.surface.get_width()-TextSurf.get_width())//2,
                                     (self.surface.get_height()-TextSurf.get_height())//2))
        self.parent_surface.blit(self.surface, self.coords)

    def set_coords(self, new_coords):
        # Sets the coords variable to the sqpecified coords
        self.coords = new_coords
        
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

    def __init__(self, listOfTokens = [], limit = 1000000):
        # initializes the cache from the list of tokens (assuming no two have the same color)
        self.cache = {}
        self.gemColors = ["black", "red", "green", "blue", "white", "gold"]
        for color in self.gemColors:
            self.cache[color] = Token(color)
        for token in listOfTokens:
            self.cache[token.get_gemColor()] = Token(token.get_gemColor(), token.get_num())
        self.limit = limit

    def get_num(self, color):
        # gets the number of tokens of a color
        return self.cache[color].get_num()

    def get_total_num(self):
        # gets the total number of tokens
        return sum([self.get_num(color) for color in self.cache.keys()])

    def get_limit(self):
        # gets the token limit
        return self.limit

    def receive(self, increment):
        # attempts to increase token count, where increment is a TokenCache
        # returns True if successful
        # returns False if token limit is reached (usually meaning the player has to get rid of some tokens)
        for color in get_colors().keys():
            self.cache[color].increase(increment.get_num(color))
        return self.get_total_num() <= self.limit

    def give(self, decrement):
        # attempts to decrease token count, where decrement is a TokenCache
        # returns True if successful
        # returns False if not enough tokens; the giving does not happen
        # Note: always run the giving function before the receiving function
        for color in get_colors().keys():
            if self.get_num(color) < decrement.get_num(color):
                return False
        for color in get_colors().keys():
            self.cache[color].decrease(decrement.get_num(color))
        return True

    def numSelected(self):
        pass

class CardCache:

    def __init__(self, listOfCards = []):
        # initializes cache given a list of cards
        # will need to implement a one-use-card cache (for expansion)
        self.cache = {}
        self.gemColors = ["black", "red", "green", "blue", "white", "gold"]
        self.cache = {color: [] for color in self.gemColors}
        for card in listOfCards:
            # currently assumes only one kind of gem at a time
            gem_count = card.get_gem_count()
            gem = ""
            for color in gem_count.keys():
                if gem_count[color] > 0:
                    gem += color
            self.cache[gem].append(card)

    def get_cache(self):
        # gets the cache (as a dictionary mapping colors to lists of cards)
        return self.cache

    def get_num(self, color):
        # gets the total number of gems of a given color
        return sum([card.get_gem_count()[color] for card in self.cache[color]])

    def get_num_cards(self):
        # gets the total number of cards
        return sum([len(self.cache[color]) for color in self.cache.keys()])

    def get_num_points(self):
        # gets the total number of points (in the cards)
        return sum([sum(card.get_points() for card in self.cache[color]) for color in self.cache.keys()])

    def get_gems(self):
        # returns a TokenCache object symbolizing the coverage of the cards as gem engines
        return_me = TokenCache()
        for color in self.gemColors:
            print("In CardCache class:", color, self.get_num(color))
            t = Token(color, self.get_num(color))
            tc = TokenCache([t])
            return_me.receive(tc)
        return return_me

    def add_card(self, card):
        # adds card to cache
        # currently assumes only one kind of gem at a time
        gem_count = card.get_gem_count()
        gem = ""
        for color in gem_count.keys():
            if gem_count[color] > 0:
                gem += color
        self.cache[gem].append(card)

class Player:

    def __init__(self, ID, reserveLimit = 3, tokenLimit = 10):
        # initialize variables to defaults for a player
        # (will need to implement nobles)
        # (will need to implement a one-use cardCache for expansion)
        self.ID = ID
        self.reserveLimit = reserveLimit
        self.tokenCache = TokenCache([], tokenLimit)
        self.cardCache = CardCache()
        self.reservedCards = []

    def get_cards(self):
        # gets the cardCache variable
        return self.cardCache

    def get_tokens(self):
        # gets the tokenCache variable
        return self.tokenCache

    def get_reservedCards(self):
        # gets the reservedCards variable
        return self.reservedCards

    def receiveTokens(self, tokens):
        # gains tokens (tokens is a TokenCache object)
        # returns True/False based on the receive() function from TokenCache class
        return self.tokenCache.receive(tokens)

    def spendTokens(self, tokens):
        # attempts to spend tokens (supposedly on something, or discard excess maybe) (tokens is a TokenCache object)
        # returns True/False based on the give() function from TokenCache class
        return self.tokenCache.give(tokens)

    def get_numFromCards(self, color):
        # gets the number of gems of given color just using the cardCache
        return self.cardCache.get_num(color)

    def get_points(self):
        # gets the number of points
        # (will need to modify once nobles is implemented)
        return self.cardCache.get_num_points()

    def gainTokens(self, tokens):
        # gains the given tokens (TokenCache object)
        # returns false if limit exceeded, true otherwise
        return self.tokenCache.receive(tokens)

    def giveTokens(self, tokens):
        # gives the given tokens (TokenCache object)
        # returns true if successful, false if unsuccessful
        return self.tokenCache.give(tokens)

    def gainCard(self, card):
        # gains card into cardCache
        self.cardCache.add_card(card)

    def canReserveCard(self):
        # returns whether a card may be reserved
        return len(self.reservedCards) < self.reserveLimit

    def reserveCard(self, card):
        # reserves card into reservedCards, up to reserveLimit (in which card will not be reserved)
        # returns True if successful, False if unsuccessful
        if not self.canReserveCard():
            return False
        self.reservedCards.append(card)
        return True

    def pickReserveCard(self, index):
        # removes and returns the card of that index in the reserved cards
        return self.reservedCards.pop(index)

    def gainReserveCard(self, index):
        # gains card in reserves
        card = self.reservedCards.pop(index)
        self.gainCard(card)

# Test code
"""
game_surface = pygame.display.set_mode((1440,900)) 
game_surface.fill((255,255,255))
k = Token("blue", 3, game_surface, [100, 100])
k.draw()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
"""

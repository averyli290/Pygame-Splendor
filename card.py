import pygame
from general_functions import *

pygame.font.init()
pygame.init()

class Card:
    cost = {"black": 0,
            "red": 0,
            "green": 0,
            "blue": 0,
            "white": 0}
    gem_count = {"black": 0,
            "red": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "gold": 0}
    
    colors = get_colors()
    
    default_font_size = 20 

    def __init__(self, parent_surface, cost, gem_count, points=0, one_use_only=False, category=0, coords=[0,0], width=141, height=200):
        # Sets up all of the variable needed for the card 
        # Creating the surface for the card
        
        self.parent_surface = parent_surface
        for gem in cost: self.cost[gem] += cost[gem]
        for gem in gem_count: self.gem_count[gem] += gem_count[gem]
        self.points = points 
        self.one_use_only = one_use_only
        self.category = category
        self.width = width
        self.height = height 
        self.coords = coords

        self.font_size = int(height*self.default_font_size/200)
       
        self.surface = pygame.Surface((width,height)) 
        self.surface.fill((200,200,200))
        
    def draw(self):
        # Draws the card onto the parent surface

        drawx = 0; drawy = self.surface.get_height()
        textcolor = (200,200,200); font = pygame.font.get_default_font(); italic = True; rotation=0

        for color in self.cost:
            if self.cost[color] > 0:
                TextSurf, TextRect = display_text(str(self.cost[color]),self.font_size,font,textcolor,italic,rotation)
                textwidth, textheight = TextSurf.get_size()
                drawx = int(textwidth)
                drawy -= int(TextSurf.get_height()*1.5)
                pygame.draw.circle(self.surface,self.colors[color],(drawx+textwidth//2,drawy+textheight//2),textwidth)
                self.surface.blit(TextSurf,(drawx, drawy))

        self.parent_surface.blit(self.surface, self.coords)

    def move(self, new_coords):
        # Sets the coords variable to the specified coordinates
        self.coords = new_coords

game_surface = pygame.display.set_mode((1440,900)) 

cost = {"black": 1,
        "red": 1,
        "green": 0,
        "blue": 0,
        "white": 0}
gem_count = {"black": 0,
        "red": 0,
        "green": 0,
        "blue": 0,
        "white": 0,
        "gold": 0}

c = Card(game_surface, cost, gem_count, 0, False, 1, [100, 100])

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    game_surface.fill((7,79,26))
    c.draw()
    pygame.display.flip()

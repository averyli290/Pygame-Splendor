import pygame
from general_functions import *

pygame.font.init()
pygame.init()

class Card:
    
    colors = get_colors()

    def __init__(self, parent_surface, cost, gem_count, points=0, one_use_only=False, category=0, coords=[0,0], width=141, height=200):
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

        self.default_font_size0 = 20 ; self.default_font_size1 = 25 # Two font sizes for the cards

        self.parent_surface = parent_surface
        for gem in cost: self.cost[gem] += cost[gem]
        for gem in gem_count: self.gem_count[gem] += gem_count[gem]
        self.points = points 
        self.one_use_only = one_use_only
        self.category = category
        self.width = width
        self.height = height 
        self.coords = coords

        self.font_size0 = int(height*self.default_font_size0/200)
        self.font_size1 = int(height*self.default_font_size1/200)
       
        self.surface = pygame.Surface((width,height)) 
        self.cardcolor = (200,200,200)
        self.surface.fill(self.cardcolor)
        
    def draw(self):
        # Draws the card onto the parent surface with cost and type 

        drawx = 0; drawy = self.surface.get_height()
        textcolor = (200,200,200); font = pygame.font.get_default_font(); italic = True; rotation=0

        for color in self.cost:
            if self.cost[color] > 0:
                TextSurf, TextRect = display_text(str(self.cost[color]),self.font_size0,font,textcolor,italic,rotation)
                textwidth, textheight = TextSurf.get_size()
                drawx = int(textwidth)
                drawy -= int(TextSurf.get_height()*1.5)
                pygame.draw.circle(self.surface,(255,255,255),(drawx+textwidth//2,drawy+textheight//2),textwidth)
                pygame.draw.circle(self.surface,self.colors[color],(drawx+textwidth//2,drawy+textheight//2),int(textwidth*0.99))
                self.surface.blit(TextSurf,(drawx, drawy))
        
        drawx = int(self.surface.get_width()*1.05); drawy = 0
        for color in self.gem_count:
             if self.gem_count[color] > 0:
                for i in range(self.gem_count[color]):
                    TextSurf, TextRect = display_text(str(self.cost[color]),self.font_size1,font,self.colors[color],False,rotation)
                    textwidth, textheight = TextSurf.get_size()
                    drawx -= int(textwidth*2)
                    drawy = int(textheight)//10
                    pygame.draw.circle(self.surface,(255,255,255),(drawx+textwidth//2,drawy+textheight//2),textwidth)
                    pygame.draw.circle(self.surface,self.colors[color],(drawx+textwidth//2,drawy+textheight//2),int(textwidth*0.99))
                    self.surface.blit(TextSurf,(drawx, drawy))
        self.parent_surface.blit(self.surface, self.coords)

    def move(self, new_coords):
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


###############
## TEST CODE ##
###############
'''
game_surface = pygame.display.set_mode((1440,900)) 

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


c = Card(game_surface, cost, gem_count, 0, False, 1, [100, 100])
c.draw()
c.move((200,200))

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    game_surface.fill((7,79,26))
    c.draw()
    pygame.display.flip()
'''

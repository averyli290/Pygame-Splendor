import pygame

pygame.font.init()

def text_objects(text, font, color, rotation=0):
    textSurface = font.render(text, True, color)
    textSurface = pygame.transform.rotate(textSurface, rotation)
    return textSurface, textSurface.get_rect()

def display_text(text, size, font, color, italic=False, rotation=0):
    torender = pygame.font.Font(font, size)
    torender.set_italic(italic)
    TextSurf, TextRect = text_objects(text, torender, color, rotation)
    TextRect.center = (0, 0) 
    return TextSurf, TextRect

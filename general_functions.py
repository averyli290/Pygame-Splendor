import pygame

pygame.font.init()

def get_colors():
    colors_dict = {}
    
    lines = []
    with open("colors.txt", "r") as colors:
        for line in colors:
            lines.append(line)

    for line in lines:
        color, rgb_val = line.split(";")
        rgb_val = eval(rgb_val)
        colors_dict[color] = rgb_val

    return colors_dict

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

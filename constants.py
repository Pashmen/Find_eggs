import pygame
from pathlib import Path

WINDOW_WIDTH_IN_PIXELS = 640
WINDOW_HEIGHT_IN_PIXELS = 480
CELL_SIZE = 20

EGGS_NUMBER = 5

FPS = 30

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
GREEN =         (100, 204, 100)
RED   =         (200,   0,   0)
BLUE  =         (100, 100, 255)  
GRAY  =         (220, 220, 220)
DARK_GRAY =     (100, 100, 100)
GOLD  =         (255, 223,   0)
ORANGE =        (255, 105,   0)

pygame.mixer.init()
SOUNDS = {'egg_is_taken' : pygame.mixer.Sound(str(Path('Resources/Sounds/') / 'egg_is_taken.ogg')),
          'cutters_are_exploded' : pygame.mixer.Sound(str(Path('Resources/Sounds/') / 'cutters_are_exploded.ogg')),
          'is_win' : pygame.mixer.Sound(str(Path('Resources/Sounds/') / 'is_win.ogg')),
          'pseudo_cutter_is_constructed' : pygame.mixer.Sound(str(Path('Resources/Sounds/') / 'pseudo_cutter_is_constructed.ogg')),
          'snake_is_eaten' : pygame.mixer.Sound(str(Path('Resources/Sounds/') / 'snake_is_eaten.ogg'))}

import sys, pygame
from pygame.locals import *

def check_for_quit():
    if len(pygame.event.get(QUIT)) != 0:
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        pygame.event.post(event)

import pygame
from constants import *
from other import *


def draw_cell(surface, x, y, color):
    pygame.draw.rect(surface, color, (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))
    

def draw_hero_coords(surface, hero, font):
    coords_surf = font.render('x:%3d y:%3d' % (hero.x, hero.y), True, DARK_GRAY)

    coords_rect = coords_surf.get_rect()
    coords_rect.topleft = (10, 10)

    surface.blit(coords_surf, coords_rect)


def draw_eggs_info(surface, eggs_number, taken_eggs_number, font):    
    info_surf = font.render("%d / %d" % (taken_eggs_number, eggs_number), True, DARK_GRAY)

    info_rect = info_surf.get_rect()
    info_rect.topleft = (10, 30)

    surface.blit(info_surf, info_rect)


def draw_help_info(surface, font):
    help_surf = font.render("Press h for help", True, DARK_GRAY)

    help_rect = help_surf.get_rect()
    help_rect.topleft = (10, 50)

    surface.blit(help_surf, help_rect)
    

def draw_saving(surface, font):
    saving_surf = font.render("Saving ...", True, DARK_GRAY)

    saving_rect = saving_surf.get_rect()
    saving_rect.topleft = (10, 70)

    surface.blit(saving_surf, saving_rect)


def draw_help(surface, font, fps_clock):       
    text = \
''' It's a world where you can move a hero with arrow keys 
 Your task is to take 5 eggs out of 5 

 About keys 
  ss  - press s twice to save the world 
  d   - press d to download your saved world 
  n   - press n to restart the game
  a   - press a to get advice
  h   - press h to get the help page
  Esc - press Esc to exit 

 About the left top corner: 
   x: 10 y:  7  - means the hero coordinates
   2 / 5   -  means you've taken 2 eggs out of 5

 Press any key to continue the game
'''

    surface.fill(BLACK)
    LINE_HEIGHT = 20
    y = 1
    lines = text.split('\n')
    
    for line in lines:
        if line != '':    
            line_surf = font.render(line, True, WHITE)
            line_rect = line_surf.get_rect()
            line_rect.topleft = (5, y * LINE_HEIGHT)

            surface.blit(line_surf, line_rect)

        y += 1

    while True:
        check_for_quit()
        if len(pygame.event.get(KEYDOWN)) > 0:
            break
        
        pygame.event.get()
        pygame.display.update()
        fps_clock.tick(FPS)


def draw_advice(surface, advice_font, press_font, fps_clock, eggs, last_advice_number):    
    ''' Returns the number of the last used advice'''
    
    advice_number = None
    for i in range(1, EGGS_NUMBER + 1):
        advice_number = (last_advice_number + i) % EGGS_NUMBER
        if not eggs[advice_number].is_taken:
            break

    surface.fill(BLACK)

    advice_surf = advice_font.render(eggs[advice_number].advice, True, WHITE)
    advice_rect = advice_surf.get_rect()
    advice_rect.center = (WINDOW_WIDTH_IN_PIXELS // 2, WINDOW_HEIGHT_IN_PIXELS // 2)
    surface.blit(advice_surf, advice_rect)

    advice_surf = press_font.render('Press any key to continue the game', True, GRAY)
    advice_rect = advice_surf.get_rect()
    advice_rect.center = (WINDOW_WIDTH_IN_PIXELS // 2, WINDOW_HEIGHT_IN_PIXELS // 2 + 40)
    surface.blit(advice_surf, advice_rect)
    
    while True:
        check_for_quit()
        if len(pygame.event.get(KEYDOWN)) > 0:
            break
        
        pygame.event.get()
        pygame.display.update()
        fps_clock.tick(FPS)
    
    return advice_number


def draw_win(surface, font):
    win_surf = font.render("WIN!", True, GOLD)

    win_rect = win_surf.get_rect()
    win_rect.center = (WINDOW_WIDTH_IN_PIXELS // 2, WINDOW_HEIGHT_IN_PIXELS // 2)

    surface.blit(win_surf, win_rect)

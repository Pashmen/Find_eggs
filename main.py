import pygame, sys, random, time, pickle
from pathlib import Path
from pygame.locals import *


from field import *
from camera import *
from eggs import *
from animals import *
from drawing import *
from square import *
from other import *


def main():        
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH_IN_PIXELS, WINDOW_HEIGHT_IN_PIXELS))
    pygame.display.set_caption("Find eggs")

    icon = pygame.image.load(str(Path('Resources/Images/') / 'icon.png')).convert_alpha()
    icon.set_colorkey(WHITE)
    pygame.display.set_icon(icon)
        
    pygame.mixer.music.load(str(Path('Resources/Sounds/') / 'background_music.ogg'))    
    pygame.mixer.music.play(-1, 0.0)
    
    basic_font = pygame.font.Font('freesansbold.ttf', 16)
    coords_font = basic_font
    eggs_font = basic_font
    saving_font = basic_font
    win_font = pygame.font.Font('freesansbold.ttf', 64)
    help_info_font = pygame.font.Font('freesansbold.ttf', 10)
    help_font = basic_font
    advice_font = basic_font
    press_font = pygame.font.Font('freesansbold.ttf', 10)

    '''
    # For testing
    hero = Hero(6, 2, BLUE)
    cutter = Cutter(15, 15, RED)
    snake = Snake(7, 15, ORANGE)
    pseudo_cutter = Pseudo_cutter(DARK_GRAY, [(1, 2), (2, 1), (2, 2), (2, 3), (4, 2)])
    
    eggs = [None] * EGGS_NUMBER  
    eggs[0] = Egg0(5, 5, 'Be fast then darkness will dissappear')    
    eggs[1] = Egg(2, 21, 'Check the labyrinth')
    eggs[2] = Egg2(12, 14, 'Try cracking the egg shell')
    eggs[3] = Egg(cutter.x + 1, cutter.y + 1, 'It likes snakes', False)
    eggs[4] = Egg(cutter.x + 1, cutter.y + 1, 'It\'s waiting for the similar creature', False)    
    '''

    hero = Hero(6, 8, BLUE)
    cutter = Cutter(15, 15, RED)
    snake = Snake(40, 15, ORANGE)
    pseudo_cutter = Pseudo_cutter(DARK_GRAY, [(1, 2), (2, 1), (40, 7), (20, 15), (10, 10)])    
    
    eggs = [None] * 5    
    eggs[0] = Egg0(45, 45, 'Be fast then darkness will disappear')
    eggs[1] = Egg(32, 46, 'Check the labyrinth')    
    eggs[2] = Egg2(40, 14, 'Try cracking the egg shell')
    eggs[3] = Egg(cutter.x + 1, cutter.y + 1, 'It likes snakes', False)
    eggs[4] = Egg(cutter.x + 1, cutter.y + 1, 'It\'s waiting for the similar creature', False)    
    
    field = Field()
    camera = Camera()    
    
    file = open(Path('Resources/Worlds/') / 'start_world.pickle', 'rb')
    world = pickle.load(file)
    field.whole_update(world[0])
    file.close()
    
    was_first_s = False
    first_s_time = None
    TIME_BETWEEN_S = 1.0

    SHOWING_SAVING_PERIOD = 2.0
    showing_saving_start_time = None

    taken_eggs_number = 0
    was_win = False

    last_advice_number = EGGS_NUMBER - 1
    
    while True:        
        check_for_quit()
        
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_s:
                # Saves the world
                if was_first_s:                    
                    if time.time() - first_s_time < TIME_BETWEEN_S:                                                
                        file = open(Path('Resources/Worlds/') / 'world.pickle', 'wb')                                
                        pickle.dump((field.cells, hero, eggs, cutter, snake, pseudo_cutter, was_win), file)
                        file.close()                       
                        
                        was_first_s = False
                        first_s_time = None

                        showing_saving_start_time = time.time()
                    else:
                        first_s_time = time.time()
                else:
                    was_first_s = True
                    first_s_time = time.time()                    
            elif event.key == K_d:
                # Downloads the saved world
                file = open(Path('Resources/Worlds/') / 'world.pickle', 'rb')                
                new_cells, hero, eggs, cutter, snake, pseudo_cutter, was_win = pickle.load(file)
                field.whole_update(new_cells)                                
                file.close()
            elif event.key == K_n:
                # Downloads the new world
                file = open(Path('Resources/Worlds/') / 'start_world.pickle', 'rb')              
                new_cells, hero, eggs, cutter, snake, pseudo_cutter, was_win = pickle.load(file)
                field.whole_update(new_cells)
                file.close()
            elif event.key == K_h:
                # Shows the help page
                draw_help(display_surf, help_font, fps_clock)
            elif event.key == K_a and taken_eggs_number < EGGS_NUMBER:
                # Shows advice                
                last_advice_number = draw_advice(display_surf, advice_font, press_font, fps_clock, eggs, last_advice_number)
            else:
                pygame.event.post(event)
                
        # It's needed to update the field information after all object.update(...), because the objects can move
        field.update(hero, eggs, cutter, snake, pseudo_cutter)

        hero.update(field, eggs, cutter, snake, pseudo_cutter)
        field.update(hero, eggs, cutter, snake, pseudo_cutter)
        
        cutter.update(field, hero, eggs)
        field.update(hero, eggs, cutter, snake, pseudo_cutter)
        
        snake.update(field, cutter, eggs)
        camera.update(hero)        


        # Draws
        display_surf.fill(BLACK)
        field.draw(display_surf, camera)
        for egg in eggs:
            egg.draw(display_surf, camera)
        hero.draw(display_surf, camera)
        cutter.draw(display_surf,camera)
        snake.draw(display_surf, camera)
        pseudo_cutter.draw(display_surf, camera)
        
        draw_hero_coords(display_surf, hero, coords_font)        

        taken_eggs_number = len([True for egg in eggs if egg.is_taken])
        draw_eggs_info(display_surf, EGGS_NUMBER, taken_eggs_number, eggs_font)
        draw_help_info(display_surf, help_info_font)
        
        # Draws saving
        if showing_saving_start_time != None:
            if time.time() - showing_saving_start_time < SHOWING_SAVING_PERIOD:
                draw_saving(display_surf, saving_font)
            else:
                showing_saving_start_time = None

        # Draws and plays sound if that's a win
        if taken_eggs_number == EGGS_NUMBER:
            draw_win(display_surf, win_font)
            
            if not was_win:
                SOUNDS['is_win'].play()
                was_win = True            
        
        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()

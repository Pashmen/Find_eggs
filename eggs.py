import time

from constants import *
from drawing import *

class Egg:
    '''
        The base class for eggs
        The hero needs to find Eggs
    '''

    # self.is_visible - if it exists for the field
    # self.is_taken - if it's taken by hero 
    # self.advice - the string with advice to show it a user if he needs advice
    def __init__(self, x, y, advice, is_visible = True):
        self.x = x
        self.y = y
        self.is_visible = is_visible
        self.is_taken = False
        self.color = GOLD        
        self.advice = advice 
        

    def update(self, hero):
        '''Returns if the hero made a step'''
        
        if not self.is_taken and self.is_visible and hero.next_step != None and [self.x, self.y] == hero.next_step:
            self.make_taken()
            hero.make_step()

            return True
        else:
            return False


    def make_visible(self):
        self.is_visible = True


    def make_taken(self):
        self.is_taken = True
        self.x = -1
        self.y = -1

        pygame.mixer.Sound.play(SOUNDS['egg_is_taken'])
        
    
    def draw(self, surface, camera):
        if self.is_visible and not self.is_taken:
            pygame.draw.circle(surface, self.color, ((self.x - camera.x) * CELL_SIZE + CELL_SIZE // 2, (self.y - camera.y) * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2 )
        

class Egg0(Egg):
    ''' It's for the specific egg which is covered by a black square in the game beginning'''
    
    def __init__(self, x, y, advice):
        Egg.__init__(self, x, y, advice)

        # These attributes are for showing the uncovered egg 
        self.is_covered = True
        self.SHOWING_PERIOD = 2
        self.showing_start_time = None

        # These attributes are for calculating whether the hero cracks the cover
        self.LAST_HERO_STEPS_NUMBER = 5
        self.last_hero_steps_times = [None] * self.LAST_HERO_STEPS_NUMBER
        self.last_hero_steps_times[-1] = time.time()


    def update(self, hero):
        '''Returns if the hero made a step'''

        # Makes the Egg taken if it's shown as uncovered enough long time
        if not self.is_taken and not self.is_covered and time.time() - self.showing_start_time > self.SHOWING_PERIOD:
            self.make_taken()
                
        if hero.next_step != None and [self.x, self.y] == hero.next_step:
            if not self.is_covered:
                self.update_times()
                hero.make_step()
            elif (self.last_hero_steps_times[0] != None) and (time.time() - self.last_hero_steps_times[0] < hero.STEP_TIME * self.LAST_HERO_STEPS_NUMBER + 0.1):                    
                self.is_covered = False    
                self.showing_start_time = time.time()
                del self.last_hero_steps_times

            return True
        else:
            return False

    
    def update_times(self):
        if self.is_covered:
            self.last_hero_steps_times.append(time.time())
            del self.last_hero_steps_times[0]
    
        
    def draw(self, surface, camera):
        if self.is_covered:
            draw_cell(surface, self.x - camera.x, self.y - camera.y, BLACK)
        else:
            if not self.is_taken:
                Egg.draw(self, surface, camera)      


class Egg2(Egg):
    ''' It's for the specific egg which is inside shell in the game beginning'''

    def __init__(self, x, y, advice):
        Egg.__init__(self, x, y, advice)
        self.shell_color = BLACK


    def update(self, field, hero, cutter):
        '''Returns if the hero made a step'''

        # Makes the Egg taken if it's in the mouth of the alive cutter
        if not self.is_taken and cutter.is_alive and (self.x, self.y) == cutter.mouth and not cutter.mouth_is_open():
            self.make_taken()
            
        if hero.next_step != None and [self.x, self.y] == hero.next_step:
            # Checks if the next cell for Egg is valid 
            next_x = 2 * self.x - hero.x
            next_y = 2 * self.y - hero.y
            if (field.is_valid(next_x, next_y) and \
            # move straight
            (self.x == next_x or self.y == next_y) or \
            # or check whether diffraction-like behaviour will not happen while attempting to move diagonally
            (field.is_valid(self.x, next_y) and field.is_valid(next_x, self.y) and \
            field.is_valid(hero.x, hero.next_step[1]) and field.is_valid(hero.next_step[0], hero.y))):                      
                self.x = next_x
                self.y = next_y
                hero.make_step()

            return True
        else:
            return False

        
    def draw(self, surface, camera):
        if not self.is_taken:
            Egg.draw(self, surface, camera)
            pygame.draw.circle(surface, self.shell_color, ((self.x - camera.x) * CELL_SIZE + CELL_SIZE // 2, (self.y - camera.y) * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 1, 1)

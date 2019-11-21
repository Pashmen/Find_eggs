import time
from pygame.locals import *

from drawing import *


class Square:
    ''' The Square can be an independent creature or a part of a creature'''
    
    def __init__(self, x, y, color):        
        self.x = x
        self.y = y            
        self.color = color        

    def draw(self, surface, camera):
        draw_cell(surface, self.x - camera.x, self.y - camera.y, self.color)        


class Hero(Square):
    ''' The Hero is a creature which is managed by the user '''
    
    def __init__(self, x, y, color):
        Square.__init__(self, x, y, color)

        self.STEP_TIME = 0.05
        self.last_step_time = time.time()
        self.next_step = None


    # The Hero moves, moves and takes eggs, moves the pseudo_cutter parts 
    def update(self, field, eggs, cutter, snake, pseudo_cutter):        
        self.next_step = None
        if time.time() - self.last_step_time > self.STEP_TIME:
            is_pressed = pygame.key.get_pressed()
            if is_pressed[K_LEFT] and self.x > 0:                
                self.next_step = (self.x - 1, self.y)
            elif is_pressed[K_RIGHT] and self.x < field.WIDTH - 1:
                self.next_step = (self.x + 1, self.y)
            elif is_pressed[K_UP] and self.y > 0:
                self.next_step = (self.x, self.y - 1)
            elif is_pressed[K_DOWN] and self.y < field.HEIGHT - 1:
                self.next_step = (self.x, self.y + 1)
            
            pygame.event.get() # Cleans the queue
            
            step_is_made = eggs[0].update(self)
            step_is_made = eggs[1].update(self) or step_is_made
            step_is_made = eggs[2].update(field, self, cutter) or step_is_made
            step_is_made = eggs[3].update(self) or step_is_made
            step_is_made = eggs[4].update(self) or step_is_made
            step_is_made = pseudo_cutter.update(field, self, eggs, cutter, snake) or step_is_made
            if not step_is_made and \
            self.next_step != None and field.is_valid(self.next_step[0], self.next_step[1]):            
                self.make_step()
                
                eggs[0].update_times() # Updates times of the last hero steps

    def make_step(self):
        self.x, self.y = self.next_step
        self.last_step_time = time.time()        


class Box(Square):
    ''' The Box is a part of the pseudo_cutter'''
    
    def update(self, field, hero):
        ''' Returns if hero made a step'''
        
        if hero.next_step != None and (self.x, self.y) == hero.next_step:
            # Checks if the next cell for the Box is valid 
            next_x = 2 * self.x - hero.x
            next_y = 2 * self.y - hero.y
            if field.is_valid(next_x, next_y):                          
                self.x = next_x
                self.y = next_y
                hero.make_step()

            return True
        else:
            return False

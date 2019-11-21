import time

from constants import *
from drawing import *
from square import *


class Snake:
    ''' It's a usual snake'''
    
    def __init__(self, x, y, color):        
        self.TIME_STEP = 0.3
        self.step_last_time = time.time()
        self.color = color

        self.direction_number = 2
        self.DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        
        self.FULL_LENGTH = 5
        self.parts = []        
        for dx in range(self.FULL_LENGTH):
            self.parts.append((x + dx, y))

    
    def update(self, field, cutter, eggs):
        ''' The Snake can make step or lose the head in the cutter mouth'''
        
        if len(self.parts) > 0 and time.time() - self.step_last_time > self.TIME_STEP:
            head = self.parts[-1]

            # Checks directions for the next step
            for number_delta in [0, 1, -1]:
                next_direction_number = (self.direction_number + number_delta) % 4                
                next_direction = self.DIRECTIONS[next_direction_number]
                next_x, next_y = (head[0] + next_direction[0], head[1] + next_direction[1])
                if field.is_valid(next_x, next_y):
                    self.direction_number = next_direction_number
                    self.step_last_time = time.time()
                    
                    self.parts.append((next_x, next_y))
                    del self.parts[0]
                    
                    return
                
            # Checks if the Snake loses its head
            if cutter.is_alive and head == cutter.mouth:
                del self.parts[0]
                self.step_last_time = time.time()

                if len(self.parts) == self.FULL_LENGTH - 1:
                    SOUNDS['snake_is_eaten'].play()

            # Makes the egg[3] visible if the Snake's died recently
            if len(self.parts) == 0:
                eggs[3].make_visible()
                for dx in range(-2, -10, -1):
                    if field.is_valid(eggs[3].x + dx, eggs[3].y):
                        eggs[3].x += dx
                        
                        return 
        

    def get_living_cells(self):
        return set(self.parts)

    def is_alive(self):
        return len(self.parts) > 0

    def draw(self, surface, camera):
        for (x, y) in self.parts:
            draw_cell(surface, x - camera.x, y - camera.y, self.color)
            

class Cutter:
    ''' It's like a crab. It opens and closes its mouth periodically. See SHAPES to understand the crab shapes'''
    
    def __init__(self, x, y, color):
        self.SHAPES = \
        [['xx ',
          ' xx',
          'xx '],

        [' x ',
         'xxx',
         ' x ']]
        
        self.CHANGES_PERIOD = 0.5
        self.change_last_time = time.time()
        self.x = x
        self.y = y
        self.mouth = (x, y + 1)        
        self.color = RED        
        self.shape_number = 0
        self.shape = self.SHAPES[self.shape_number]
        self.is_alive = True


    def update(self, field, hero, eggs):
        ''' The Cutter can open or close the mouth'''
        
        if (self.is_alive and time.time() - self.change_last_time > self.CHANGES_PERIOD):
            # Checks if nothing prevents the mouth moving
            # eggs[2] doesn't influence on the Cutter so it's in this condition
            if self.shape_number == 0 and ((eggs[2].x, eggs[2].y) == self.mouth or field.is_valid(self.mouth[0], self.mouth[1])) or \
            self.shape_number == 1 and field.is_valid(self.x, self.y) and field.is_valid(self.x, self.y + 2):
                self.shape_number = (self.shape_number + 1) % 2
                self.shape = self.SHAPES[self.shape_number]
                self.change_last_time = time.time()
                

    def get_living_cells(self):
        living_cells = set()

        if self.is_alive:
            for dy in range(len(self.shape)):
                for dx in range(len(self.shape[dy])):                
                    if self.shape[dy][dx] == 'x':
                        living_cells.add((self.x + dx, self.y + dy))

        return living_cells
    

    def mouth_is_open(self):        
        return self.shape_number == 0

           
    def draw(self, surface, camera):
        if self.is_alive: 
            for dy in range(len(self.shape)):
                for dx in range(len(self.shape[dy])):                
                    if self.shape[dy][dx] == 'x':
                        draw_cell(surface, self.x + dx - camera.x, self.y + dy - camera.y, self.color)


class Pseudo_cutter:
    '''
        In the first stage it's a set of boxes which hero can move
        If hero constructs a needed shape (like a plus), the Psuedo_cutter'll move to the cutter
        When it joins to the cutter, both the Pseudo_cutter and the cutter will disappear
    '''
    
    def __init__(self, color, points_pattern):
        self.PARTS_NUMBER = 5
        self.is_alive = True
        self.is_constructed = False
        self.color = color        
        self.parts = []
        assert len(points_pattern) == self.PARTS_NUMBER, 'Pseudo_cutter needs %d points in __init__' % self.PARTS_NUMBER
        for (x, y) in points_pattern:
            self.parts.append(Box(x, y, self.color))
        
        self.PATTERN = {(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)}
        self.STEP_TIME = 0.5
        self.step_last_time = None
        self.x = None
        self.y = None                

    def update(self, field, hero, eggs, cutter, snake):
        ''' Makes Pseudo_cutter constructed or not alive
            Returns if hero made a step
        '''
        
        if self.is_alive:
            if not self.is_constructed:
                step_is_made = False
                # Checks all parts for moving
                for part in self.parts:
                    step_is_made = part.update(field, hero) or step_is_made

                # Checks if it's constructed now
                if self.get_living_cells() == self.PATTERN:                    
                    self.is_constructed = True
                    self.step_last_time = time.time()
                    self.x = 1
                    self.y = 1
                    
                    self.color = RED
                    for part in self.parts:
                        part.color = self.color

                    SOUNDS['pseudo_cutter_is_constructed'].play()

                return step_is_made
            else:
                if time.time() - self.step_last_time > self.STEP_TIME:
                    # Checks if it moves down
                    if self.y < cutter.y:
                        if field.is_valid(self.x, self.y + 2) and field.is_valid(self.x + 1, self.y + 3) and field.is_valid(self.x + 2, self.y + 2):
                            self.make_step(0, 1)
                            field.update(hero, eggs, cutter, snake, self)
                    # Checks if it moves to the right
                    elif self.x < cutter.x - 2:
                        if field.is_valid(self.x + 2, self.y) and field.is_valid(self.x + 3, self.y + 1) and field.is_valid(self.x + 2, self.y + 2):
                            self.make_step(1, 0)
                            field.update(hero, eggs, cutter, snake, self)
                    # It's joined to the cutter. They'll disappear
                    else:
                        self.is_alive = False
                        self.parts.clear()
                        
                        cutter.is_alive = False
                        SOUNDS['cutters_are_exploded'].play()                        
                        
                        eggs[4].make_visible()
                    
                return False
        else:
            return False

         
    def get_living_cells(self):        
        living_cells = set()
        for part in self.parts:
            living_cells.add((part.x, part.y))

        return living_cells


    def make_step(self, dx, dy):
        self.x += dx
        self.y += dy
        for part in self.parts:
            part.x += dx
            part.y += dy
            
        self.step_last_time = time.time()

    
    def draw(self, surface, camera):
        for part in self.parts:
            part.draw(surface, camera)

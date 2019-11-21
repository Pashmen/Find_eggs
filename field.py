import pygame
from constants import *
from drawing import *


class Field:
    ''' The Field is space with cells where all creatures lives'''
    
    def __init__(self):
        self.WIDTH = 50
        self.HEIGHT = 50        
        self.EMPTY = 0 # It's used if a field cell hasn't an obstacle
        self.OBSTACLE = 1 # It's used if a field cell has an obstacle
        self.OBSTACLE_COLOR = GREEN
        self.living_cells = set() # It's a set of cells which are occupied by creatures
        self.whole_update()

        
    def whole_update(self, new_cells = None):
        # Updates cells
        if new_cells == None:
            self.cells = [None] * self.WIDTH
            for i in range(self.WIDTH):
                self.cells[i] = [self.EMPTY] * self.HEIGHT       
        else:
            self.cells = new_cells

        # Creates the surface with the drawn field
        self.surface = pygame.Surface((self.WIDTH * CELL_SIZE + 1, self.HEIGHT * CELL_SIZE + 1))
        self.surface.fill(WHITE)        
        
        for x in range(self.WIDTH + 1):
            pygame.draw.line(self.surface, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, self.HEIGHT * CELL_SIZE + 1))

        for y in range(self.HEIGHT + 1):
            pygame.draw.line(self.surface, GRAY, (0, y * CELL_SIZE), (self.WIDTH * CELL_SIZE + 1, y * CELL_SIZE))
        
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if self.cells[x][y] == self.OBSTACLE:
                    draw_cell(self.surface, x, y, self.OBSTACLE_COLOR)


    def update(self, hero, eggs, cutter, snake, pseudo_cutter):
        # Updates living_cells which are occupied by the creatures
        
        self.living_cells.clear()
        self.living_cells.add((hero.x, hero.y))
        for egg in eggs:            
            if egg.is_visible and not egg.is_taken: 
                self.living_cells.add((egg.x, egg.y))

        self.living_cells = self.living_cells | cutter.get_living_cells() | snake.get_living_cells() | pseudo_cutter.get_living_cells()
        
        
    def is_valid(self, x, y):
        ''' Returns if the (x, y) is within the field and the cell (x, y) hasn't an obstacle and isn't occupied by a creature'''
        
        return (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT and self.cells[x][y] != self.OBSTACLE) and (x, y) not in self.living_cells

    
    def draw(self, surface, camera):        
        surface.blit(self.surface, (-camera.x * CELL_SIZE, -camera.y * CELL_SIZE))

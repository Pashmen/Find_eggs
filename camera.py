from constants import *

class Camera:
    ''' The Camera allows to see the space near the hero'''
    
    def __init__(self):
        assert WINDOW_WIDTH_IN_PIXELS % CELL_SIZE == 0, "The window width must be divisible by cell size"
        assert WINDOW_HEIGHT_IN_PIXELS % CELL_SIZE == 0, "The window height must be divisible by cell size"
        self.WIDTH = WINDOW_WIDTH_IN_PIXELS // CELL_SIZE
        self.HEIGHT = WINDOW_HEIGHT_IN_PIXELS // CELL_SIZE
        self.WIDTH_HALF = self.WIDTH // 2
        self.HEIGHT_HALF = self.HEIGHT // 2
        self.SLACK = 5
        
        self.x = 0
        self.y = 0
        self.center_x = self.x + self.WIDTH_HALF
        self.center_y = self.y + self.HEIGHT_HALF            
        
        
    def update(self, hero):
        # If the hero is far from the camera center, the camera will follow it
        if hero.x - self.center_x > self.SLACK:
            self.center_x = hero.x - self.SLACK
            self.x = self.center_x - self.WIDTH_HALF
        if hero.x - self.center_x < -self.SLACK:
            self.center_x = hero.x + self.SLACK
            self.x = self.center_x - self.WIDTH_HALF
        if hero.y - self.center_y < -self.SLACK:
            self.center_y = hero.y + self.SLACK
            self.y = self.center_y - self.HEIGHT_HALF
        if hero.y - self.center_y > self.SLACK:
            self.center_y = hero.y - self.SLACK
            self.y = self.center_y - self.HEIGHT_HALF


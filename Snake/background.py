import pygame
from settings import *

class Background:
    def __init__(self) -> None:
        self.row = [pygame.Rect(x * tile_size, 0 * tile_size, tile_size, tile_size) for x in range(DIMENSION_X)]

    def draw_bg(self, display):
        for i in range(40):
            if i % 2 == 0:
                backwards = True
            else:
                backwards = False    
            for index, rect in enumerate(self.row):
                if backwards:
                    if index % 2 == 0:
                        pygame.draw.rect(display, 'gray22', rect)  
                    else:
                        pygame.draw.rect(display, 'gray38', rect)  
                else: 
                    if index % 2 == 0:
                        pygame.draw.rect(display, 'gray38', rect)  
                    else:
                        pygame.draw.rect(display, 'gray22', rect)         



import pygame
from pygame.math import Vector2
from settings import *

class Player:
    def __init__(self) -> None:
        super().__init__()
        self.body = [Vector2(10,20),Vector2(9,20),Vector2(8,20),Vector2(7,20)]
        self.direction = Vector2(1,0)

        self.score = 0
        self.font = pygame.font.Font('ARCADE_N.TTF', 20)
        self.extend = False
        self.stop = False

    def draw_body(self, display):
        for vector in self.body:
            vector_rect = pygame.Rect(int(vector.x * tile_size), int(vector.y * tile_size), tile_size, tile_size)
            pygame.draw.rect(display, 'blue', vector_rect)
            
    def animation_state(self):
        if self.direction != Vector2(0,0): 
            if self.extend == False:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)      
                self.body = body_copy  
            else:   
                self.body.insert(0, self.body[0] + self.direction)    
                self.extend = False        

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if self.direction != Vector2(0,1):
                self.direction = Vector2(0,-1)
        if keys[pygame.K_DOWN]:
            if self.direction != Vector2(0,-1):
                self.direction = Vector2(0,1)        
        if keys[pygame.K_LEFT]:
            if self.direction != Vector2(1,0):
                self.direction = Vector2(-1,0)
        if keys[pygame.K_RIGHT]:
            if self.direction != Vector2(-1,0):
                self.direction = Vector2(1,0) 

    def game_over(self):
        """Game over conditions"""
        if (0 > self.body[0].x or self.body[0].x > DIMENSION_X - 1) or (0 > self.body[0].y or self.body[0].y > DIMENSION_Y - 1):
            self.stop = True
            self.direction = Vector2(0,0)
            return True
        for body in self.body[1::]:
            if body == self.body[0]:
                self.stop = True
                self.direction = Vector2(0,0)
                return True
        return False 

    def draw_score(self, display):
        render = self.font.render(f'Score: {self.score}', True, 'White')     
        rect = render.get_rect(center = (GAME_RES[0] // 2, 20)) 
        display.blit(render, rect) 

    def highest_score(self):
        with open('highest_score.txt', 'r+') as file:
            file.seek(0)
            if self.score > int(file.read()):
                file.truncate()
                file.seek(0)
                file.write(str(self.score)) 
                            
    def update(self, display) -> None:
        if not self.stop:
            self.player_input()
        self.draw_body(display)
        self.draw_score(display)
        





import pygame
from pygame.math import Vector2
from settings import *
import random

class Fruit(pygame.sprite.Sprite):
    def __init__(self, player) -> None:
        super().__init__()
        self.position = Vector2(random.randint(1,39), random.randint(1,39))
        self.player = player
        
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = pygame.Rect(int(self.position.x * tile_size), int(self.position.y * tile_size), tile_size, tile_size)
        self.image.fill('red')
        self.eat_sound = pygame.mixer.Sound('eat_sfx.mp3')
        self.eat_sound.set_volume(0.2)

    def collision_detection(self):
        """Checks collision with player"""
        if self.position == self.player.body[0]:
            self.eat_sound.play()
            self.kill()
            self.player.score += 10
            self.player.extend = True    

    def update(self) -> None:
        super().update()        
        self.collision_detection()


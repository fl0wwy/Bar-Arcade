import pygame
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_sprite.png'),180,0.15)
        self.rect = self.image.get_rect(center = (640,600))
        
        self.dmg = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_sprite_dmg.png'),180,0.15)
        self.index = 0

        self.health = 3
        self.points = 0

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if self.rect.left >= 20:
                self.rect.x -= 4    
        if keys[pygame.K_d]:
            if self.rect.right <= 1260:
                self.rect.x += 4
        if pygame.mouse.get_pressed()[0]:
            if not shot_group.sprites():
                shot_group.add(Projectile('graphics/player/player_shot.png', 0.15, 5, self))  

    def animation_state(self):
        if self.image == self.dmg: 
            self.index += 0.1
            if self.index >= 1:
                self.image = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_sprite.png'),180,0.15)
                self.index = 0                             

    def update(self,display) -> None:
        super().update()     
        self.player_input()
        self.animation_state()
        shot_group.draw(display) 
        shot_group.update()              

shot_group = pygame.sprite.GroupSingle()
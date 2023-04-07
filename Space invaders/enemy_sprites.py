import pygame
from player import shot_group
from projectile import Projectile
import random
from sounds import enemy_death

class Enemy(pygame.sprite.Sprite):
    velocity = 1
    speedup = 0
    drop = False

    def __init__(self, pos, enemy, player) -> None:
        super().__init__()
        self.images = [pygame.transform.rotozoom(pygame.image.load(f'graphics/adversaries/{enemy}/1.png').convert_alpha(),0,1.2)
                       ,pygame.transform.rotozoom(pygame.image.load(f'graphics/adversaries/{enemy}/2.png').convert_alpha(),0,1.2)]
        self.index = 0

        self.image = self.images[int(self.index)]
        self.rect = self.image.get_rect(topleft = pos)

        self.starting_point_x = self.rect.centerx
        
        self.type = enemy
        self.player_sprite = player

    def animation_state(self): 
        '''Switching the frame render of the sprite'''
        self.index += 0.02
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)] 

    def move(self):
        """Moves the sprite from side to side"""
        self.rect.x += self.velocity
        if self.rect.centerx >= self.starting_point_x + 280 or self.rect.centerx <= self.starting_point_x - 280: 
            self.speedup += 1
            if self.speedup % 2 == 0:
                if self.velocity > 0:
                    self.velocity += 1
                else:
                    self.velocity -= 1      
            self.velocity *= -1
            self.drop = True

                
    def destroy(self):
        '''Checks if the sprite and the projectile the player has shot are colliding.
        if so, removes the sprite from the group and resets the player's shot'''
        if shot_group.sprite:
            if self.rect.colliderect(shot_group.sprite.rect):
                enemy_death.play()
                match self.type:
                    case '1':
                        self.player_sprite.points += 20
                    case '2':
                        self.player_sprite.points += 10
                    case 'shooter':
                        self.player_sprite.points += 40    
                    case 'ufo':
                        self.player_sprite.points += random.randint(100,300)   
                self.kill()  
                shot_group.empty() 
        if self.type == 'ufo':
            if self.rect.left <= -30:
                self.kill()                                  

    def update(self) -> None:
        super().update()   
        self.animation_state()
        self.move()
        self.destroy()
        # An addition to the movement mechanic - drops the sprite downwards.
        if self.drop:
            self.rect.y += 20
            self.drop = False 

class Shooter(Enemy):
    def __init__(self, pos, display, player, enemy='shooter') -> None:
        super().__init__(pos, enemy, player)
        self.shoot = False
        self.display = display

        self.projectile = pygame.sprite.GroupSingle()

    def shot(self):
        if self.shoot:
            if not self.projectile.sprite:
                self.projectile.add(Projectile('graphics/adversaries/shooter/enemy_shot.png', 0.15, -3, self))
            self.shoot = False
        else:
            self.shoot = random.choices([True, False], weights=[0.1,99], k=1)[0] 

        if self.projectile.sprite:
            if self.projectile.sprite.rect.colliderect(self.player_sprite):
                self.player_sprite.image = self.player_sprite.dmg
                self.projectile.empty()
                self.player_sprite.health -= 1              

    def update(self) -> None:
        super().update() 
        self.shot()  
        self.projectile.draw(self.display)
        self.projectile.update() 

class UFO(Enemy):
    def __init__(self, player, pos=(1350,20), enemy='ufo') -> None:
        super().__init__(pos, enemy, player)

    def move(self):
        self.rect.x -= 4           

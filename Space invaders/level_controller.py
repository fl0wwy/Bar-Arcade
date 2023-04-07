import pygame
from enemy_sprites import *

class LevelBuilder:
    def __init__(self, display, player) -> None:
        self.level = [
            '10101010101010101010',
            '00000000000000000000',
            '20202020202020202020',
            '00000000000000000000',
            '20202020202020202020',
            '00000000000000000000',
            '30303030303030303030',
            '00000000000000000000',
            '30303030303030303030',
        ]
        self.display = display
        self.player_sprite = player
        self.ufo = False
        
        self.level_setup()
    
    def level_setup(self):
        for row_index, row in enumerate(self.level):
            for col_index, column in enumerate(row):
                match column:
                    case '1':
                        enemy_group.add(Shooter(((col_index * 31) + 311, (row_index * 31) + 50), self.display, self.player_sprite)) 
                    case '2':  
                        enemy_group.add(Enemy(((col_index * 31) + 305, (row_index * 31) + 50), '1', self.player_sprite))  
                    case '3': 
                        enemy_group.add(Enemy(((col_index * 31) + 305, (row_index * 31) + 50), '2', self.player_sprite))  
    def level_run(self):
        if not self.ufo:
            self.ufo = random.choices([True,False], weights=[0.1,99],k=1)[0]
            if self.ufo:
                if not ufo.sprite:
                    ufo.add(UFO(self.player_sprite))
                self.ufo = False    
        
        enemy_group.draw(self.display)
        enemy_group.update()   
        ufo.draw(self.display)
        ufo.update()                  

enemy_group = pygame.sprite.Group()
ufo = pygame.sprite.GroupSingle()

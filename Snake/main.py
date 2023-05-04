import pygame
from sys import exit
from settings import *
from player import Player
from fruit import Fruit

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.display = pygame.display.set_mode(GAME_RES)
        self.clock = pygame.time.Clock()
       
        self.player = Player()
        self.TRIGGER_MOVEMENT = pygame.USEREVENT
        pygame.time.set_timer(self.TRIGGER_MOVEMENT, 100)
        self.fruit = pygame.sprite.GroupSingle(Fruit(self.player))

        self.game_active = False
        self.game_over = False
        self.font = pygame.font.Font('ARCADE_N.TTF', 30)
        self.font_small = pygame.font.Font('ARCADE_N.TTF', 20)
        self.font_large = pygame.font.Font('ARCADE_N.TTF', 50) 
        self.game_over_sound = pygame.mixer.Sound('gameover_sfx.mp3')
        self.game_over_sound.set_volume(0.2)

    def event_checker(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() 
            if event.type == self.TRIGGER_MOVEMENT:
                self.player.animation_state()
            if event.type == pygame.KEYDOWN: 
                    if self.game_over == True or self.game_active == False:
                        if self.game_over == True:
                            self.player = Player()
                            self.fruit.add(Fruit(self.player))   
                        self.game_active = True
                        self.game_over = False

    def update(self):
        pygame.display.update()
        self.clock.tick(60)
        pygame.display.set_caption(str(round(self.clock.get_fps(),2)))
    
    def draw_background(self):
        """Draws the background tiles"""
        for y in range(40):
            row = [pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size) for x in range(DIMENSION_X)]
            if y % 2 == 0:
                backwards = True
            else:
                backwards = False    
            for index, rect in enumerate(row):
                if backwards:
                    if index % 2 == 0:
                        pygame.draw.rect(self.display, 'gray10', rect)  
                    else:
                        pygame.draw.rect(self.display, 'gray19', rect)  
                else: 
                    if index % 2 == 0:
                        pygame.draw.rect(self.display, 'gray19', rect)  
                    else:
                        pygame.draw.rect(self.display, 'gray10', rect)      

    def get_high_score(self):
        with open('highest_score.txt', 'r') as file:
            file.seek(0)
            return file.read()    
    
    def new_game(self):
        while True:
            self.draw_background() 
            self.event_checker()

            # Sprite renders
            self.player.update(self.display)
            self.fruit.draw(self.display)
            self.fruit.update()

            # Initializing new fruit
            if self.fruit.sprites() == []:
                self.fruit.add(Fruit(self.player))
            
            if self.game_over == False:
                if self.player.game_over() == True: 
                    self.game_over_sound.play()
                    self.game_over = True
                    self.game_active = False
                
            # Game over screen
            if self.game_over: 
                self.player.highest_score()
                hscore_render = self.font.render(f'Highest Score: {self.get_high_score()}', True, 'White')
                hscore_rect = hscore_render.get_rect(center = (GAME_RES[0] // 2 , 300))

                restart = self.font_small.render('press any key to restart', True, 'White')
                restart_rect = restart.get_rect(center = (GAME_RES[0] // 2 , 500))

                headline = self.font_large.render('GAME OVER', True, 'White')
                headliie_rect = headline.get_rect(center = (GAME_RES[0] // 2 , 100))
                
                self.display.blit(headline, headliie_rect)
                self.display.blit(hscore_render, hscore_rect)    
                self.display.blit(restart, restart_rect)
            
            self.update()

if __name__ == '__main__':
    game = Game()
    game.new_game()

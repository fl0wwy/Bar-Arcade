import pygame
from sys import exit
from player import Player
from level_controller import *
from bg_animation import Background
from sounds import *

# Init
pygame.init()
display = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(pygame.image.load('graphics/adversaries/1/1.png'))
theme.play(-1)

# Sprites
player = pygame.sprite.GroupSingle(Player())
level = LevelBuilder(display, player.sprite)
background_animation = Background(display)
earth = pygame.image.load('graphics/background/earth.png').convert_alpha()
earth_rect = earth.get_rect(midbottom = (640,720))

# Fonts
data_font = pygame.font.Font('graphics/ARCADE_N.TTF', 20)
title_font = pygame.font.Font('graphics/ARCADE_N.TTF', 50) 
button_font = pygame.font.Font('graphics/ARCADE_N.TTF', 30)

# Score editing functions
def read_score():
    with open('high_score.txt', 'r') as file:
        file.seek(0)
        return file.read()

def write_score(zero=False):
    with open('high_score.txt', 'r+') as file:
        file.seek(0)
        if not zero:
            if int(file.read()) < player.sprite.points:
                file.truncate(0)
                file.seek(0)
                file.write(str(player.sprite.points))  
        else:
            file.truncate(0)
            file.seek(0)
            file.write('0')        

# Title screen
title_screen = True

title_text = title_font.render('SPACE INVADERS', True, 'White')
title_text_rect = title_text.get_rect(center = (640, 100))

high_score_text = data_font.render(f'HIGH SCORE<{read_score()}>', True, 'White') 
high_score_text_rect = high_score_text.get_rect(center = (640, 20))    

start_button = button_font.render('START', True, 'White') 
start_button_rect = start_button.get_rect(center = (640, 500))

# Pause menu
pause_menu = False

pause_text = title_font.render('Game Paused', True, 'White')
pause_text_rect = pause_text.get_rect(center = (640, 100))

reset_button = button_font.render('RESET', True, 'White')
reset_button_rect = reset_button.get_rect(center = (640,300))

reset_score = button_font.render('CLEAR HIGH SCORE', True, 'White')
reset_score_rect = reset_score.get_rect(center = (640,400))

exit_button = button_font.render('EXIT', True, 'White')
exit_button_rect = exit_button.get_rect(center = (640,500))

game_active = False

# Game over
game_over = False

game_over_text = title_font.render('GAME OVER', True, 'White')
game_over_text_rect = game_over_text.get_rect(center = (640, 100))

try_again_button = button_font.render('Play Again?', True, 'White')
try_again_button_rect = try_again_button.get_rect(center = (640, 250))

# You win
win = False

win_text = title_font.render('YOU WIN', True, 'White')
win_text_rect = win_text.get_rect(center = (640, 100))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not title_screen and not game_over:
                    if pause_menu == False:
                        pause_menu = True
                    else:
                        pause_menu = False
                        game_active = True         

    # Displaying background
    background_animation.animation()
    display.blit(earth,earth_rect)
    
    # Retreiving mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Game over conditions
    for enemy_sprite in enemy_group.sprites():
        if enemy_sprite.rect.colliderect(earth_rect):
            game_over = True
    if player.sprite.health == 0:
        game_over = True  
    # Win condition
    if enemy_group.sprites() == []: 
        win = True      

    # Game states    
    if game_active:
        # Sprites
        player.draw(display)
        player.update(display)
        level.level_run()
        # Information text
        score = data_font.render(f'SCORE<{player.sprite.points}>', True, 'White')
        score_rect = score.get_rect(topleft = (10,10))
        health = data_font.render(f'HEALTH<{player.sprite.health}>', True, 'White')
        health_rect = score.get_rect(center = (1180,20))
        display.blit(score,score_rect)
        display.blit(health,health_rect)
    
    if title_screen:
        if start_button_rect.collidepoint(mouse_pos):
            start_button = button_font.render('START', True, 'Green') 
            if pygame.mouse.get_pressed()[0]:
                title_screen = False
                game_active = True 
        else:    
            start_button = button_font.render('START', True, 'White') 
        display.blit(title_text,title_text_rect)   
        display.blit(start_button,start_button_rect)     
    
    if pause_menu:
        game_active = False 
        # Restart the game
        if reset_button_rect.collidepoint(mouse_pos):
            reset_button = button_font.render('RESET', True, 'Green') 
            if pygame.mouse.get_pressed()[0]:
                write_score()
                high_score_text = data_font.render(f'HIGH SCORE<{read_score()}>', True, 'White') 
                
                player.sprite = Player()
                enemy_group.empty()
                level = LevelBuilder(display, player.sprite)
                
                pause_menu = False
                game_active = True
        else:
            reset_button = button_font.render('RESET', True, 'White') 
        # Reset the score
        if reset_score_rect.collidepoint(mouse_pos):
            reset_score = button_font.render('Clear High Score', True, 'Green') 
            if pygame.mouse.get_pressed()[0]:
                write_score(True)
                high_score_text = data_font.render(f'HIGH SCORE<{read_score()}>', True, 'White') 
        else:
            reset_score = button_font.render('Clear High Score', True, 'White') 
        # Exit the game
        if exit_button_rect.collidepoint(mouse_pos):
            exit_button = button_font.render('EXIT', True, 'green') 
            if pygame.mouse.get_pressed()[0]:
                write_score()
                pygame.quit()
                exit()   
        else:
            exit_button = button_font.render('EXIT', True, 'White') 
     
        display.blit(pause_text,pause_text_rect)  
        display.blit(reset_button,reset_button_rect)
        display.blit(reset_score,reset_score_rect)
        display.blit(exit_button,exit_button_rect)
    
    if game_over or win:
        game_active = False
        # Try again
        if try_again_button_rect.collidepoint(mouse_pos):
            try_again_button = button_font.render('Play Again?', True, 'Green') 
            if pygame.mouse.get_pressed()[0]:
                write_score()
                high_score_text = data_font.render(f'HIGH SCORE<{read_score()}>', True, 'White') 
                
                player.sprite = Player()
                enemy_group.empty()
                level = LevelBuilder(display, player.sprite)
                
                game_over = False
                win = False
                game_active = True
        else:
            try_again_button = button_font.render('Play Again?', True, 'White') 
        # Exit the game
        if exit_button_rect.collidepoint(mouse_pos):
            exit_button = button_font.render('EXIT', True, 'green') 
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                exit()      
        else:
            exit_button = button_font.render('EXIT', True, 'White') 
        
        write_score()
        high_score_text = data_font.render(f'HIGH SCORE<{read_score()}>', True, 'White') 
        if game_over:
            display.blit(game_over_text,game_over_text_rect) 
        elif win:
            display.blit(win_text,win_text_rect)     
        display.blit(try_again_button,try_again_button_rect)  
        display.blit(exit_button,exit_button_rect) 

    # Displaying high score    
    display.blit(high_score_text,high_score_text_rect)
    
    # Updating the display and setting FPS
    pygame.display.update()
    clock.tick(60)                    

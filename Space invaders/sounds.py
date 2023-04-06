import pygame

pygame.mixer.init()

theme = pygame.mixer.Sound('graphics/game_theme.mp3')
theme.set_volume(0.15)
enemy_death = pygame.mixer.Sound('graphics/adversaries/death.mp3')
enemy_death.set_volume(0.15)
import pygame

# Sounds
pygame.mixer.init()
paddle = pygame.mixer.Sound('materials/paddle.mp3')
wall = pygame.mixer.Sound('materials/wall.mp3')
paddle.set_volume(0.1)
wall.set_volume(0.1)

class Player(pygame.sprite.Sprite):
    def __init__(self,side=0,p1=True) -> None:
        super().__init__()
        self.image = pygame.Surface((10,50))
        self.image.fill(pygame.Color('cornsilk'))
        self.rect = self.image.get_rect(center = (side,200))

        self.p1 = p1
        self.score = 0

        self.font = pygame.font.Font('materials/font.TTF',30)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.p1:
            control = [pygame.K_w,pygame.K_s]
        else:
            control = [pygame.K_UP,pygame.K_DOWN]   

        if keys[control[0]]:
            if not self.rect.collidepoint((self.rect.x,0)):
                self.rect.y -= 5
        if keys[control[1]]:
            if not self.rect.collidepoint((self.rect.x,400)):
                self.rect.y += 5  
    def scoreboard(self,display,x_axis):
        text = self.font.render(f'{self.score}',True,pygame.Color('darkseagreen1')) 
        text_rect = text.get_rect(center = (x_axis,20)) 
        display.blit(text,text_rect) 
    
    def update(self) -> None:
        super().update()
        self.player_input()

class Player_2(Player):
    def __init__(self, side=800, p1=False) -> None:
        super().__init__(side, p1)  

class Ball(pygame.sprite.Sprite):    
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect(center = (400,200))

        self.direction = False
        self.angle = 0

    def animation(self,player,p2):     
        self.rect.y += self.angle
        
        if not self.direction:
            self.rect.x -= 10
            
            if self.rect.colliderect(player.rect):
                pygame.mixer.Sound.play(paddle)
                self.direction = True

                if self.rect.centery < player.rect.centery:
                    self.angle = (abs(self.rect.centery - player.rect.centery) * -1) / 10
                elif self.rect.centery > player.rect.centery:   
                    self.angle = abs(self.rect.centery - player.rect.centery) / 10  
                else:
                    self.angle = 0    
        if self.direction:
            self.rect.x += 10

            if self.rect.colliderect(p2.rect):
                pygame.mixer.Sound.play(paddle)
                self.direction = False  

                if self.rect.centery < p2.rect.centery:
                    self.angle = (abs(self.rect.centery - p2.rect.centery) * -1) / 10
                elif self.rect.centery > p2.rect.centery:   
                    self.angle = abs(self.rect.centery - p2.rect.centery) / 10  
                else:
                    self.angle = 0  
        
        if self.rect.collidepoint((self.rect.x,400)) or self.rect.collidepoint((self.rect.x,0)):
            pygame.mixer.Sound.play(wall)
            self.angle = self.angle * -1                 

    def update(self, display,game_state,player,p2) -> None:
        super().update(display)
        pygame.draw.ellipse(display,pygame.Color('cornsilk'),self.rect)
        if game_state:
            self.animation(player,p2)              
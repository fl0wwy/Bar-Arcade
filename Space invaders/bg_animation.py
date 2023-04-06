import pygame

class Background():
    def __init__(self, display) -> None:
        self.images = [pygame.image.load('graphics/background/bg_1.png').convert_alpha()
                       ,pygame.image.load('graphics/background/bg_2.png').convert_alpha()]
        self.rect_1 = self.images[0].get_rect(topleft = (0,0))
        self.rect_2 = self.images[0].get_rect(topleft = (0,720))

        self.display = display
        
    def animation(self):
        self.display.blit(self.images[0],self.rect_1)
        self.display.blit(self.images[1],self.rect_2)

        self.rect_1.y -= 1
        self.rect_2.y -= 1
        if self.rect_1.bottom <= 0:
            self.rect_1.top = 720
        if self.rect_2.bottom <= 0:
            self.rect_2.top = 720

            



import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, size, velocity, entity) -> None:
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(image).convert_alpha(), 0 , size)
        self.rect = self.image.get_rect(center = entity.rect.center)

        self.velocity = velocity

    def animation_state(self):
        self.rect.y -= self.velocity

        if self.rect.bottom <= -20 or self.rect.top >= 740:
            self.kill()

    def update(self) -> None:
        super().update()   
        self.animation_state()             
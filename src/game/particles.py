import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self,pos):
        super(Particle, self).__init__()
        self.image = pygame.Surface((4,4), pygame.SRCALPHA)
        self.image.fill((255, random.randint(100,200), 0))
        self.rect = self.image.get_rect(center = pos)
        self.velocity = [random.uniform(-2,2), random.uniform(-2,2)]
        self.lifetime = 30

    def update(self):
        self.rect.x +=self.velocity[0]
        self.rect.y += self.velocity[1]
        self.lifetime -=1
        if self.lifetime <=0:
            self.kill()

import pygame
import random
from constants import LANE_X_POSITION
enemyImages = [
    "assets/images/Mark 1 - Ash.png",
    "assets/images/Mark 1 - Bleed.png",
    "assets/images/Mark 1 - Jet.png",
    "assets/images/Mark 1 - Rush.png",
    "assets/images/Mark 1 - Scarlet.png"
]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, lane_idx):
        super(Enemy, self).__init__()
        imagePath = random.choice(enemyImages)
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*1.5, self.image.get_height()*1.5))
        self.rect = self.image.get_rect()
        self.rect.centerx = LANE_X_POSITION[lane_idx]
        self.rect.y = -self.rect.height
        self.vel_x = 0
        self.vel_y = random.randrange(3,8)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


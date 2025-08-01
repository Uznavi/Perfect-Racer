import pygame
import random
import src.system.constants as c
from src.utilities import resource_path

enemyImages = [
    "assets/images/Mark 1 - Ash.png",
    "assets/images/Mark 1 - Bleed.png",
    "assets/images/Mark 1 - Jet.png",
    "assets/images/Mark 1 - Rush.png",
    "assets/images/Mark 1 - Scarlet.png"
]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, lane_idx, scaler):
        super(Enemy, self).__init__()
        self.scaler = scaler
        imagePath = random.choice(enemyImages)
        self.image = pygame.image.load(resource_path(imagePath))
        DESIGN_CAR_WIDTH = 40 
        DESIGN_CAR_HEIGHT = 85
        scaled_w, scaled_h = self.scaler.scale_size(DESIGN_CAR_WIDTH, DESIGN_CAR_HEIGHT)
        self.image = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        self.rect = self.image.get_rect()
        self.rect.centerx, _ = self.scaler.scale_pos(c.LANE_X_POSITION[lane_idx], 0)
        self.rect.y = -self.rect.height
        self.vel_x = 0
        self.vel_y = random.randrange(3, 8)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
import pygame
import random
import src.system.constants as c
from src.utilities import resource_path

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, lane_idx, scaler):
        super(ItemBox, self).__init__()
        self.scaler = scaler 
        DESIGN_BOX_SIZE = 40 
        self.image = pygame.image.load(resource_path("assets/images/itemBox.png"))
        scaled_w, scaled_h = self.scaler.scale_size(DESIGN_BOX_SIZE, DESIGN_BOX_SIZE)
        self.image = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        self.rect = self.image.get_rect()
        self.rect.centerx, _ = self.scaler.scale_pos(c.LANE_X_POSITION_BOXES[lane_idx], 0)
        self.rect.y = -self.rect.height
        self.vel_x = 0
        self.vel_y = 8
        self.hit = False
        self.powerUp = random.choice(c.POWER_UPS)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
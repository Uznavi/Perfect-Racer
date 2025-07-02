import pygame
import random
from constants import LANE_X_POSITION_BOXES, POWER_UPS


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, lane_idx):
        super(ItemBox, self).__init__()
        self.image = pygame.image.load("assets/images/itemBox.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()/40, self.image.get_height()/40))
        self.rect = self.image.get_rect()
        self.rect.centerx = LANE_X_POSITION_BOXES[lane_idx]
        self.rect.y = -self.rect.height
        self.vel_x = 0
        self.vel_y = 5
        self.hit = False
        self.powerUp = random.choice(POWER_UPS)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


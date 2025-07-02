import pygame
import random
from constants import LANE_X_POSITION_BOXES
from itemBox import ItemBox

class ItemBoxSpawner():
    def __init__(self):
        self.itemBox_group = pygame.sprite.Group()
        self.itemBox_spawn_timer = random.randrange(300, 600)
    
    def update(self):
        self.itemBox_group.update()
        if self.itemBox_spawn_timer == 0:
            self.spawnItemBox()
            self.itemBox_spawn_timer = random.randrange(300, 600)
        else:
            self.itemBox_spawn_timer -=1
    
    def spawnItemBox(self):
        for laneX in range(len(LANE_X_POSITION_BOXES)):
            item_box = ItemBox(laneX)
            self.itemBox_group.add(item_box)

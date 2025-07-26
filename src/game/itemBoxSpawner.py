import pygame
import random
import src.system.constants as c
import time
from src.game.itemBox import ItemBox

class ItemBoxSpawner():
    def __init__(self, scaler):
        self.scaler = scaler  # Store scaler for use in methods
        self.itemBox_group = pygame.sprite.Group()
        self.itemBox_spawn_timer = 15
        self.lastSpawnTime = time.time()
    
    def update(self):
        self.itemBox_group.update()
        currentTime = time.time()
        if currentTime - self.lastSpawnTime >= self.itemBox_spawn_timer:
            self.spawnItemBox()
            self.lastSpawnTime = currentTime
    
    def spawnItemBox(self):
        for laneX in range(len(c.LANE_X_POSITION_BOXES)):
            item_box = ItemBox(laneX, self.scaler)
            self.itemBox_group.add(item_box)
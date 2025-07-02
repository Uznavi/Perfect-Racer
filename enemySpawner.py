import pygame
import random
from constants import LANE_X_POSITION
from enemyCar import Enemy

class EnemySpawner:
    def __init__(self):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = random.randrange(30, 60)
    
    def update(self):
        self.enemy_group.update()
        if self.spawn_timer == 0:
            self.spawnEnemy()
            self.spawn_timer = random.randrange(30, 60)
        else:
            self.spawn_timer -=1
    def spawnEnemy(self):
        #You're gonna be able to tell that this part was made by Copilot
        #This just checks that a car can spawn in a disoccupied lane cuz i don't want them to overlap and shit
        minDistanceY = 435
        minDistanceX = 40
        freeLanes = []
        for idx, lane_x in enumerate(LANE_X_POSITION):
            lane_free = True
            for enemy in self.enemy_group:
                if (
                    abs(enemy.rect.x - lane_x) < minDistanceX and 
                    abs(enemy.rect.y + enemy.rect.height) < minDistanceY
                ):
                    lane_free = False
                    break
            if lane_free:
                freeLanes.append(idx)
        if freeLanes:
            lane_idx = random.choice(freeLanes)
            newEnemy = Enemy(lane_idx)
            self.enemy_group.add(newEnemy)
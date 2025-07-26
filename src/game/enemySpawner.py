import pygame
import random
import src.system.constants as c
from src.game.enemyCar import Enemy

class EnemySpawner:
    def __init__(self, scaler):
        self.scaler = scaler  # Store scaler for use in methods
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = random.randrange(30, 60)
    
    def update(self):
        self.enemy_group.update()
        if self.spawn_timer == 0:
            self.spawnEnemy()
            self.spawn_timer = random.randrange(30, 60)
        else:
            self.spawn_timer -= 1

    def spawnEnemy(self):
        _, minDistanceY = self.scaler.scale_pos(0, 435)
        minDistanceX, _ = self.scaler.scale_pos(40, 0)
        freeLanes = []
        for idx, lane_x in enumerate(c.LANE_X_POSITION):
            scaled_lane_x, _ = self.scaler.scale_pos(lane_x, 0)
            lane_free = True
            for enemy in self.enemy_group:
                if (
                    abs(enemy.rect.x - scaled_lane_x) < minDistanceX and 
                    abs(enemy.rect.y + enemy.rect.height) < minDistanceY
                ):
                    lane_free = False
                    break
            if lane_free:
                freeLanes.append(idx)
        if freeLanes:
            lane_idx = random.choice(freeLanes)
            newEnemy = Enemy(lane_idx, self.scaler)
            self.enemy_group.add(newEnemy)
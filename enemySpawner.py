import pygame
import random
import constants as c
from enemyCar import Enemy
from scaler import scaler

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
            self.spawn_timer -= 1

    def spawnEnemy(self):
        # Use scaled distances
        _, minDistanceY = scaler.scale_pos(0, 435)
        minDistanceX, _ = scaler.scale_pos(40, 0)
        freeLanes = []
        for idx, lane_x in enumerate(c.LANE_X_POSITION):
            scaled_lane_x, _ = scaler.scale_pos(lane_x, 0)
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
            newEnemy = Enemy(lane_idx)
            self.enemy_group.add(newEnemy)
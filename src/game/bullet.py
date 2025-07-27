import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, scaler):
        super(Bullet, self).__init__()
        self.scaler = scaler 
        self.width = 8
        self.height = 16
        scaled_w, scaled_h = self.scaler.scale_size(self.width, self.height)
        self.width = scaled_w
        self.height = scaled_h
        self.image = pygame.Surface((scaled_w, scaled_h))
        self.color = (255, 0, 0)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.vel_x = 0
        _, self.vel_y = self.scaler.scale_pos(0, -5)
        self.vel_y = int(self.vel_y)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.bottom < 0:
            self.kill()
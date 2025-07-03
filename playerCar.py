import pygame
from scaler import scaler

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerCar, self).__init__()
        self.image = pygame.image.load("assets/images/PlayerCar.png").convert_alpha()
        DESIGN_CAR_WIDTH = 40   # or whatever looks good for your lanes
        DESIGN_CAR_HEIGHT = 70  # adjust as needed
        scaled_w, scaled_h = scaler.scale_size(DESIGN_CAR_WIDTH, DESIGN_CAR_HEIGHT)
        self.image = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        self.rect = self.image.get_rect()
        #645 is the middle of the screen
        #615 is the bottom of the screen
        self.rect.centerx, self.rect.centery = scaler.scale_pos(655, 608)
        self.vel_x = 0 #initial speeds
        self.vel_y = 0
        self.speed = 5 # Speed of movement, will be changed depending on the feel
                       # Depending on the playtests, I'll change it, but at the same time, it feels good, so it won't be changed :D
        self.powerUpReceived = None
        self.shieldActive = False
        self.shieldCoolDownTimer = 0

    def update(self):
        self.rect.centerx += self.vel_x
        min_x, _ = scaler.scale_pos(545, 0)
        max_x, _ = scaler.scale_pos(765, 0)
        _, min_y = scaler.scale_pos(0, 40)
        _, max_y = scaler.scale_pos(0, 608)

        if self.rect.centerx <= min_x:
            self.rect.centerx = min_x
        if self.rect.centerx >= max_x:
            self.rect.centerx = max_x
        self.rect.centery += self.vel_y
        if self.rect.centery >= max_y:
            self.rect.centery = max_y
        if self.rect.centery <= min_y:
            self.rect.centery = min_y
        if self.shieldCoolDownTimer > 0:
            self.shieldCoolDownTimer -= 1

    
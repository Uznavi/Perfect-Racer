import pygame
from scaler import scaler
from bullet import Bullet

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerCar, self).__init__()
        self.image = pygame.image.load("assets/images/PlayerCar.png").convert_alpha()
        DESIGN_CAR_WIDTH = 40 
        DESIGN_CAR_HEIGHT = 85  # adjust as needed
        scaled_w, scaled_h = scaler.scale_size(DESIGN_CAR_WIDTH, DESIGN_CAR_HEIGHT)
        self.image = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = scaler.scale_pos(655, 680)
        self.bullets = pygame.sprite.Group()
        self.vel_x = 0 #initial speeds
        self.vel_y = 0
        self.speed = 5 # Speed of movement, will be changed depending on the feel
                       # Depending on the playtests, I'll change it, but at the same time, it feels good, so it won't be changed :D
        self.powerUpReceived = None
        self.shieldActive = False
        self.shieldSoundPlayed = False
        self.bulletsActive = False
        self.bulletAmount = 20
        self.bulletSound = pygame.mixer.Sound("assets/sounds/shootingSound.ogg")
        self.shieldCoolDownTimer = 0
        self.lastBulletTime = 0
        self.bulletCooldown = 200
        self.last_input = "none"
        self.isCheating = False

    def update(self):
        self.bullets.update()
        self.rect.centerx += self.vel_x
        min_x, _ = scaler.scale_pos(535, 0)
        max_x, _ = scaler.scale_pos(775, 0)
        _, min_y = scaler.scale_pos(0, 40)
        _, max_y = scaler.scale_pos(0, 680)

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

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.bulletsActive and self.bulletAmount > 0:
            if current_time - self.lastBulletTime >= self.bulletCooldown:
                newBullet = Bullet()
                newBullet.rect.centerx = self.rect.centerx
                newBullet.rect.bottom = self.rect.top 
                self.bullets.add(newBullet)
                self.lastBulletTime = current_time
                self.bulletSound.play()
                self.bulletAmount -=1
                if self.bulletAmount <= 0:
                    self.bulletsActive = False
                    self.bulletAmount = 20
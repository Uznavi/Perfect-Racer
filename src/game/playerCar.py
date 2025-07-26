import pygame
from src.utilities import resource_path
from src.game.bullet import Bullet

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self, scaler):
        super(PlayerCar, self).__init__()
        self.scaler = scaler
        self.image = pygame.image.load(resource_path("assets/images/PlayerCar.png"))
        DESIGN_CAR_WIDTH = 40
        DESIGN_CAR_HEIGHT = 85
        self.image = pygame.transform.scale(self.image, (DESIGN_CAR_WIDTH, DESIGN_CAR_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.scaler.scale_pos(655, 680)
        self.bullets = pygame.sprite.Group()
        self.vel_x = 0 #initial speeds
        self.vel_y = 0
        self.speed = 5 # Speed of movement, will be changed depending on the feel
        self.powerUpReceived = None
        self.shieldActive = False
        self.shieldTimer = 10
        self.shieldRemaining = 0
        self.shieldStartTime = None
        self.shieldSoundPlayed = False
        self.shieldSound = pygame.mixer.Sound(resource_path("assets/sounds/shield.ogg"))
        self.bulletsActive = False
        self.bulletAmount = 20
        self.bulletSound = pygame.mixer.Sound(resource_path("assets/sounds/shootingSound.ogg"))
        self.shieldCoolDownTimer = 0
        self.lastBulletTime = 0
        self.bulletCooldown = 200
        self.bombActive = False
        self.last_input = "none"
        self.isCheating = False

    def update(self):
        self.bullets.update()
        self.rect.centerx += self.vel_x
        min_x, _ = self.scaler.scale_pos(530, 0)
        max_x, _ = self.scaler.scale_pos(781, 0)
        _, min_y = self.scaler.scale_pos(0, 40)
        _, max_y = self.scaler.scale_pos(0, 680)

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
        if self.bulletsActive and (self.bulletAmount > 0 or self.isCheating):
            if current_time - self.lastBulletTime >= self.bulletCooldown:
                newBullet = Bullet(self.scaler)
                newBullet.rect.centerx = self.rect.centerx
                newBullet.rect.bottom = self.rect.top 
                self.bullets.add(newBullet)
                self.lastBulletTime = current_time
                self.bulletSound.play()
                if not self.isCheating:
                    self.bulletAmount -=1
                    if self.bulletAmount <= 0:
                        self.bulletsActive = False
import pygame

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerCar, self).__init__()
        self.image = pygame.image.load("assets/images/PlayerCar.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*1.5, self.image.get_height()*1.5))
        self.rect = self.image.get_rect()
        #645 is the middle of the screen
        #675 is the bottom of the screen
        self.rect.centerx = 608
        self.rect.centery = 675
        self.vel_x = 0 #initial speeds
        self.vel_y = 0
        self.speed = 5 # Speed of movement, will be changed depending on the feel
                       # Depending on the playtests, I'll change it, but at the same time, it feels good, so it won't be changed :D

    def update(self):
        #Adding velocity to the coordinates to make movement
        self.rect.centerx += self.vel_x
        #500 for the left, 715 for the right
        if self.rect.centerx <= 530:
            self.rect.centerx = 530
        if self.rect.centerx >= 755:
            self.rect.centerx = 755
        self.rect.centery += self.vel_y
        if self.rect.centery >= 675:
            self.rect.centery = 675
        if self.rect.centery <=40:
            self.rect.centery = 40

    
import pygame

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerCar, self).__init__()
        self.image = pygame.image.load("assets/images/PlayerCar.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*1.5, self.image.get_height()*1.5))
        self.rect = self.image.get_rect()
        #605 is the middle of the screen
        #550 is the bottom of the screen
        self.rect.x = 605
        self.rect.y = 625
        self.vel_x = 0 #initial speeds
        self.vel_y = 0
        self.speed = 5 # Speed of movement, will be changed depending on the feel
                       # Depending on the playtests, I'll change it, but at the same time, it feels good, so it won't be changed :D

    def update(self):
        #Adding velocity to the coordinates to make movement
        self.rect.x += self.vel_x
        #500 for the left, 715 for the right
        if self.rect.x <= 500:
            self.rect.x = 500
        if self.rect.x >= 715:
            self.rect.x = 715
        self.rect.y += self.vel_y
        if self.rect.y >= 625:
            self.rect.y = 625
        if self.rect.y <=0:
            self.rect.y = 0

    
import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def getImage(self, frame, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        return image
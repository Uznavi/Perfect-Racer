import pygame
import constants as c
from scaler import GameScaler
from screens import mainMenu, profile_game

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.joystick.init()
if pygame.joystick.get_count():
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
scaler = GameScaler(c.game_width, c.game_height, screen)
game_surface = pygame.Surface((c.game_width, c.game_height))

if __name__ == "__main__":
    # mainMenu(screen, clock, joystick)
    mainMenu(screen, game_surface, clock, joystick, scaler)
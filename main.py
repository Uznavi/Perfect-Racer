import pygame
import src.system.constants as c
from src.system.scaler import GameScaler
from src.system.screens import mainMenu, profile_game

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
scaler = GameScaler(screen.get_width(), screen.get_height(), screen) # Use the actual screen dimensions for the scaler :3
game_surface = pygame.Surface((c.game_width, c.game_height))

if __name__ == "__main__":
    # mainMenu(screen, clock, joystick)
    mainMenu(screen, game_surface, clock, joystick, scaler)
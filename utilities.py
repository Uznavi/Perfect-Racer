import pygame
import constants as c

font_cache = {}
text_cache = {}

def get_font(fontSize):
    if fontSize not in font_cache:
        font_cache[fontSize] = pygame.font.Font("assets/font/PressStart2P.ttf", fontSize)
    return font_cache[fontSize]

def get_cached_text(text, fontSize, textCol):
    key = (text, fontSize, textCol)
    if key not in text_cache:
        font = get_font(fontSize)
        text_surface = font.render(text, True, textCol)
        text_cache[key] = text_surface
    return text_cache[key]

def drawText(text, fontSize, textCol, x, y, surface, scaler):
    text_surface = get_cached_text(text, fontSize, textCol)
    surface.blit(text_surface, scaler.scale_pos(x,y))

def blitScaled(game_surface, screen, scaler):
    display_width, display_height = screen.get_size()
    scale_x = display_width / c.game_width
    scale_y = display_height / c.game_height
    scale = min(scale_x, scale_y)

    scaled_width = int(c.game_width * scale)
    scaled_height = int(c.game_height * scale)

    x_offset = (display_width - scaled_width) // 2
    y_offset = (display_height - scaled_height) // 2

    scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_width , scaled_height))
    screen.fill((0,0,0))
    screen.blit(scaled_surface, (x_offset, y_offset))
    pygame.display.flip()
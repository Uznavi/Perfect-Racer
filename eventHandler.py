import pygame

def handle_main_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "play"
            if event.key == pygame.K_SPACE:
                return "controls"
            if event.key == pygame.K_ESCAPE:
                return "quit"
    return None

def handle_controls_screen_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "main_menu"
            if event.key == pygame.K_ESCAPE:
                return "quit"
    return None

def handle_game_over_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            if event.key == pygame.K_RETURN:
                return "play"
            if event.key == pygame.K_SPACE:
                return "main_menu"
    return None

def handle_pause_screen_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            if event.key == pygame.K_RETURN:
                return "resume"
    return None

def handle_gameplay_events(player, showHitboxes):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit", showHitboxes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "pause", showHitboxes
            if event.key == pygame.K_a:
                player.vel_x = -player.speed
            if event.key == pygame.K_d:
                player.vel_x = player.speed
            if event.key == pygame.K_w:
                player.vel_y = -player.speed
            if event.key == pygame.K_s:
                player.vel_y = player.speed
            if event.key == pygame.K_y and player.powerUpReceived is not None:
                if player.powerUpReceived == "shield":
                    player.shieldActive = True
                player.powerUpReceived = None
            if event.key == pygame.K_h:
                showHitboxes = not showHitboxes
            if event.key == pygame.K_ESCAPE:
                return "quit", showHitboxes
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.vel_x = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.vel_y = 0
    return None, showHitboxes
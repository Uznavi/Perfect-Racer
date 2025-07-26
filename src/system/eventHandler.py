import pygame
import src.system.constants as c
import time

cheatInput = []
cheatCode = c.CHEAT_CODE
cheatMode = False
def handle_main_menu_events():
    global cheatInput, cheatCode, cheatMode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit", cheatMode
        if event.type == pygame.KEYDOWN:
            keyMap = {
                pygame.K_w: "up",
                pygame.K_s : "down",
                pygame.K_a : "left",
                pygame.K_d : "right",
                pygame.K_q : "b",
                pygame.K_e : "a"
                }
            if event.key == pygame.K_RETURN:
                return "play", cheatMode
            if event.key == pygame.K_SPACE:
                return "controls", cheatMode
            if event.key == pygame.K_ESCAPE:
                return "quit", cheatMode
            
            if event.key in keyMap:
                cheatInput.append(keyMap[event.key])
                if len(cheatInput) > len(cheatCode):
                    cheatInput.pop(0)
                if cheatInput == cheatCode:
                    cheatMode = True
        if event.type == pygame.JOYBUTTONDOWN:
            buttonMap = {
                c.NS_D_PAD_UP : "up",
                c.NS_D_PAD_DOWN: "down",
                c.NS_D_PAD_LEFT : "left",
                c.NS_D_PAD_RIGHT : "right",
                c.NS_B : "b",
                c.NS_A: "a",
                c.PS_X : "b",
                c.PS_O : "a"
            }
            if event.button in buttonMap:
                cheatInput.append(buttonMap[event.button])
                if len(cheatInput) > len(cheatCode):
                    cheatInput.pop(0)
                if cheatInput == cheatCode:
                    cheatMode = True

            if event.button == c.NS_START:
                return "play", cheatMode
            if event.button == c.NS_SELECT:
                return "controls", cheatMode
            if event.button == c.NS_HOME:
                return "quit", cheatMode
    return None, cheatMode

def handle_controls_screen_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "main_menu"
            if event.key == pygame.K_ESCAPE:
                return "quit"
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == c.NS_SELECT:
                return "main_menu"
            if event.button == c.NS_HOME:
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
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == c.NS_START:
                return "play"
            if event.button == c.NS_SELECT:
                return "main_menu"
            if event.button == c.NS_HOME:
                return "quit"
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
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == c.NS_START:
                return "resume"
            if event.button == c.NS_HOME:
                return "quit"
    return None

def handle_gameplay_events(player, showHitboxes):
    for event in pygame.event.get():
        # Keyboard input
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
            if event.key == pygame.K_y:
                if player.powerUpReceived == "shield" and not player.shieldActive:
                    player.shieldActive = True
                    player.shieldStartTime = int(time.time())
                    player.shieldRemaining = player.shieldTimer
                    player.shieldSound.play()
                    player.shieldSoundPlayed = True
                    player.powerUpReceived = None
                    # player.powerUpReceived = None
                elif player.powerUpReceived == "bomb":
                    player.bombActive = True
                    return "bomb", showHitboxes
                elif player.powerUpReceived == "bullets":
                    player.bulletsActive = True
                    player.bulletAmount = 20
                    player.lastBulletTime = pygame.time.get_ticks()
                    player.powerUpReceived = None
                elif player.bulletsActive:
                    player.shoot()
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

        # Analog stick movement
        if event.type == pygame.JOYAXISMOTION:
            if abs(event.value) > 0.2:
                player.last_input = "analog"
                if event.axis == 0:
                    player.vel_x = player.speed * event.value
                if event.axis == 1:
                    player.vel_y = player.speed * event.value
            else:
                if event.axis == 0 and player.last_input == "analog":
                    player.vel_x = 0
                if event.axis == 1 and player.last_input == "analog":
                    player.vel_y = 0

        # D-Pad movement (button down)
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == c.NS_Y or event.button == c.PS_SQUARE:
                if player.powerUpReceived == "shield" and not player.shieldActive:
                    player.shieldActive = True
                    player.shieldStartTime = int(time.time())
                    player.shieldRemaining = player.shieldTimer
                    player.shieldSound.play()
                    player.shieldSoundPlayed = True
                    player.powerUpReceived = None
                elif player.powerUpReceived == "bomb":
                    player.bombActive = True
                    return "bomb", showHitboxes
                elif player.powerUpReceived == "bullets":
                    player.bulletsActive = True
                    player.bulletAmount = 20
                    player.lastBulletTime = pygame.time.get_ticks()
                    player.powerUpReceived = None
                elif player.bulletsActive:
                    player.shoot()
                player.powerUpReceived = None
            if event.button == c.NS_START:
                return "pause", showHitboxes
            if event.button == c.NS_HOME:
                return "quit", showHitboxes
            if event.button == c.NS_D_PAD_LEFT:
                player.last_input = "dpad"
                player.vel_x = -player.speed
            if event.button == c.NS_D_PAD_RIGHT:
                player.last_input = "dpad"
                player.vel_x = player.speed
            if event.button == c.NS_D_PAD_UP:
                player.last_input = "dpad"
                player.vel_y = -player.speed
            if event.button == c.NS_D_PAD_DOWN:
                player.last_input = "dpad"
                player.vel_y = player.speed

        # D-Pad movement (button up)
        if event.type == pygame.JOYBUTTONUP:
            if (event.button == c.NS_D_PAD_LEFT or event.button == c.NS_D_PAD_RIGHT) and player.last_input == "dpad":
                player.vel_x = 0
            if (event.button == c.NS_D_PAD_UP or event.button == c.NS_D_PAD_DOWN) and player.last_input == "dpad":
                player.vel_y = 0

    return None, showHitboxes
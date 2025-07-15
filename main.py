import pygame, sys
import spritesheet
import eventHandler
# from itemBox import ItemBox
from scaler import GameScaler, set_scaler
#TODO : At the end, clean up the main file and add stuff to other files, like constants and stuff
#TODO: DELETE ALL CHATGPT OR COPILOT COMMENTS
pygame.init()
pygame.mixer.init()
fps = 60
clock = pygame.time.Clock()
pygame.joystick.init()
if pygame.joystick.get_count():
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None
# highScore = 0
#For now I'll keep these guys here, after the initial playtesting I'll decide to bring them back
#That being said if I need to bring them back, then I'll have to scale it all over again, fml
#HEY YOU! PLAYTESTER! JUST LIKE IT THIS WAY, PLEASE
#P.S. why are you reading this? you fucking nerd ☝️🤓

#Screen constants
# screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screenWidth = 1300
screenHeight = 645
#Sprite Sheet Information and Text Color
imageSpriteSheet = pygame.image.load("assets/images/B i g  r o a d.png").convert_alpha()
spriteSheet = spritesheet.SpriteSheet(imageSpriteSheet)
textColor = (255,255,255)
#Animation process
animationList = []
animationLoop = 5
animationCooldown = 10
scaler = GameScaler(screenWidth, screenHeight, screen)
set_scaler(scaler)

from playerCar import PlayerCar
from enemySpawner import EnemySpawner
from itemBoxSpawner import ItemBoxSpawner
from particles import Particle
from scoreSystem import loadHighScore, saveHighScore

FRAME_WIDTH = 100
FRAME_HEIGHT = 100

# Try 1.1 or 1.2 for a little extra height, or 1.0 for exact fit
HEIGHT_MULTIPLIER = 1.1

for x in range(animationLoop):
    # 1. Calculate scale factor to match (or exceed) screen height
    scale_factor = (screenHeight / FRAME_HEIGHT) * HEIGHT_MULTIPLIER
    scaled_w = int(FRAME_WIDTH * scale_factor)
    scaled_h = int(FRAME_HEIGHT * scale_factor)
    # 2. Extract and scale the frame
    frame_img = spriteSheet.getImage(x, FRAME_WIDTH, FRAME_HEIGHT)
    frame_img = pygame.transform.scale(frame_img, (scaled_w, scaled_h))
    animationList.append(frame_img)

#Text function
#TODO: At some point, make a constant x and y variable to not add a new one every time
def drawText(text, fontSize, textCol, x, y):
    scaledFontSize = scaler.scale_font(fontSize)
    font = pygame.font.Font("assets/font/PressStart2P.ttf", fontSize)
    text_surface = font.render(text, True, textCol)
    scaledX, scaledY = scaler.scale_pos(x, y)
    screen.blit(text_surface, scaler.scale_pos(x,y))
#Screen Event Handlers

def gameOverScreen(score):
    previousHighScore = loadHighScore()
    if score > previousHighScore:
        pygame.mixer.music.load("assets/sounds/newHighScoreSong.mp3")
        pygame.mixer.music.play()
        resultMessage = "You are the perfect racer! Congratulations!"
        saveHighScore(score)
    else:
        resultMessage = "You are not the perfect racer! Try again!"
        pygame.mixer.music.load("assets/sounds/gameOverSong.ogg")
        pygame.mixer.music.play()
    screen.fill((0,0,0))
    drawText("YOU CRASHED!", 40, (255,0,0), 405, 185)
    drawText(f"Your score: {score}", 20, textColor, 490, 340)
    drawText(f"High Score: {previousHighScore}", 20, textColor, 490, 360)
    drawText(resultMessage, 15, textColor, 350, 400)
    drawText("To try again, press Start/Enter", 15, textColor, 400, 500)
    drawText("To go to the menu, press Select/Space", 15, textColor, 400, 520)
    drawText("To quit, press the Home button or Escape key", 15, textColor, 400, 540) 
    pygame.display.update()
    gameOverState = True
    while gameOverState:
        action = eventHandler.handle_game_over_events()
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "play":
            playScreen()
            return
        elif action == "main_menu":
            mainMenu()
            return


def pauseScreen():
    pygame.mixer.music.load("assets/sounds/pause.ogg")
    pygame.mixer.music.play()
    paused = True

    # DO NOT fill the screen again inside the loop
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # 128 = 50% transparent
    screen.blit(overlay, (0, 0))
    drawText("PAUSED", 40, textColor, 525, 300)
    drawText("Press Start/Enter to resume", 20, textColor, 380, 400)
    pygame.display.update()
    clock.tick(10)

    while paused:
        action = eventHandler.handle_pause_screen_events()
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "resume":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/sounds/gameSong.mp3")
            pygame.mixer.music.play(-1)
            return "resume"


def playScreen():
    #TODO: Since this is the meat and bones of the game, try to make it clearer what is an object and what is the object update function
    pygame.display.set_caption("Game")
    pygame.mixer.music.load("assets/sounds/gameSong.mp3")
    pygame.mixer.music.play(-1)
    shieldSound = pygame.mixer.Sound("assets/sounds/shield.ogg")
    hitSound = pygame.mixer.Sound("assets/sounds/explosion.wav")
    run = True
    lastUpdate = pygame.time.get_ticks()
    frame = 0
    score = 0
    showHitboxes = False
    high_score = loadHighScore()

    #Game objects
    player = PlayerCar()
    enemy_spawner = EnemySpawner()
    # item_box = ItemBox()
    itemBox_spawner = ItemBoxSpawner()
    particles = pygame.sprite.Group()
    spriteGroup = pygame.sprite.Group()
    spriteGroup.add(player)

    while run:
        screen.fill((50,50,50))
        clock.tick(fps)
        score +=1

        currentTime = pygame.time.get_ticks()
        if currentTime - lastUpdate >= animationCooldown:
            frame +=1
            lastUpdate = currentTime
            if frame >= len(animationList):
                frame = 0
        screen_width, screen_height = screen.get_size()
        frame_image = animationList[frame]
        x = (screen_width - frame_image.get_width()) // 2
        y = (screen_height - frame_image.get_height()) // 2
        screen.blit(frame_image, (x, y))
        drawText(f"High Score: {high_score}", 15, textColor, 1015, 430)
        drawText(f"Score: {score}", 20, textColor, 1025, 450)
        if player.powerUpReceived is not None or player.bulletsActive:
            activePowerUp = player.powerUpReceived if player.powerUpReceived is not None else "bullets"
            drawText(f"Power Up : {activePowerUp}", 15, textColor, 1010, 475)

        #Game over cause
        if pygame.sprite.spritecollideany(player, enemy_spawner.enemy_group):
            if player.shieldActive:
                player.shieldActive = False
                player.shieldSoundPlayed = False
                player.shieldCoolDownTimer = 60
            elif player.bulletsActive:
                player.bulletsActive = False
                player.shieldCoolDownTimer = 60
            elif player.shieldCoolDownTimer == 0:
                gameOverScreen(score)
        

        #Item box hitting logic
        item_box_hit = pygame.sprite.spritecollideany(player, itemBox_spawner.itemBox_group)
        if item_box_hit:
            if not player.shieldActive and not player.bulletsActive and player.powerUpReceived is None:
                player.powerUpReceived = item_box_hit.powerUp
            item_box_hit.kill()
        
        if player.shieldActive and not player.shieldSoundPlayed:
            shieldSound.play()
            player.shieldSoundPlayed = True
        
        if player.shieldActive:
            shieldSurface = pygame.Surface((player.rect.width*2, player.rect.height*2), pygame.SRCALPHA)
            pygame.draw.ellipse(
                shieldSurface,
                (100, 200, 255, 120),
                shieldSurface.get_rect()
            )
            shield_rect = shieldSurface.get_rect(center = player.rect.center)
            screen.blit(shieldSurface, shield_rect)
        
        if showHitboxes:        
            for enemy in enemy_spawner.enemy_group:
                pygame.draw.rect(screen, (255,0,0), enemy.rect, 2)
                pygame.draw.rect(screen, (0,255,0), player.rect, 2)

        action, showHitboxes = eventHandler.handle_gameplay_events(player, showHitboxes)
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "pause":
            result = pauseScreen()
            if result == "quit":
                pygame.quit()
                sys.exit()


        spriteGroup.draw(screen)
        spriteGroup.update()
        player.bullets.update()
        player.bullets.draw(screen)
        enemy_spawner.enemy_group.draw(screen)
        enemy_spawner.update()
        hits = pygame.sprite.groupcollide(player.bullets, enemy_spawner.enemy_group, True, True)
        if hits:
            score +=100
            hitSound.play()
            for enemy_list in hits.values():
                for enemy in enemy_list:
                    for _ in range(15):
                        particles.add(Particle(enemy.rect.center))
        itemBox_spawner.itemBox_group.draw(screen)
        itemBox_spawner.update()
        particles.update()
        particles.draw(screen)
        pygame.display.update()

def controlsMenu():
    pygame.display.set_caption("Controls")
    run = True
    while run:
        screen.fill((0,0,0))
        clock.tick(fps)
        drawText("CONTROLS", 40, textColor, 495, 125)
        drawText("D-Pad / WASD: Directional Movement (Up, Down, Left, Right)", 20, textColor, 70, 350)
        drawText("Y/Triangle: Power-Up (Can only be used when in inventory)", 20, textColor, 80, 395)
        drawText("This game supports DualSense, Switch Pro Controller, and LG Dual Action", 15, textColor, 125, 450)
        drawText("Press Select/Space again to go back to the title screen", 10, textColor, 370, 500)
        action = eventHandler.handle_controls_screen_events()
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "main_menu":
            mainMenu()
            return
        pygame.display.update()

def mainMenu():
    pygame.display.set_caption("Main Menu")
    # Load and play music once at the start
    pygame.mixer.music.load("assets/sounds/introSong.mp3")
    pygame.mixer.music.play()
    run = True
    while run:
        clock.tick(fps)
        screen.fill((0,0,255))
        drawText("PERFECT RACER", 40, textColor, 380, 175)
        drawText("Press Start/Enter to begin", 20, textColor, 400, 395)
        drawText("Or press Select/Space for the controls!", 20, textColor, 265, 455)
        drawText("To quit, press the Home button or Escape key", 20, textColor, 215, 515)
        action = eventHandler.handle_main_menu_events()
        if action == "play":
            playScreen()
            return
        elif action == "controls":
            controlsMenu()
            return
        elif action == "quit":
            pygame.quit()
            sys.exit()
        pygame.display.update()

mainMenu()
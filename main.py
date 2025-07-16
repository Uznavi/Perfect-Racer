#TODO : If the game looks better on the screens, fix all the squishiness and boundaries
import io
import pstats
import pygame
import cProfile
import spritesheet
import eventHandler
import constants as c
import sys
# from itemBox import ItemBox
from scaler import GameScaler, set_scaler
#TODO : At the end, clean up the main file and add stuff to other files, like constants and stuff
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
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_width, display_height = screen.get_size()
game_width, game_height = 1300, 720
game_surface = pygame.Surface((game_width, game_height))
#Sprite Sheet Information and Text Color
imageSpriteSheet = pygame.image.load("assets/images/B i g  r o a d.png").convert_alpha()
spriteSheet = spritesheet.SpriteSheet(imageSpriteSheet)
textColor = (255,255,255)
#Animation process
animationList = []
animationLoop = 5
animationCooldown = 10
scaler = GameScaler(game_width, game_height, game_surface)
set_scaler(scaler)

from playerCar import PlayerCar
from enemySpawner import EnemySpawner
from itemBoxSpawner import ItemBoxSpawner
from particles import Particle
from scoreSystem import loadHighScore, saveHighScore

FRAME_WIDTH = 100
FRAME_HEIGHT = 100
HEIGHT_MULTIPLIER = 1.1

for x in range(animationLoop):
    scale_factor = (game_height / FRAME_HEIGHT) * HEIGHT_MULTIPLIER
    scaled_w = int(FRAME_WIDTH * scale_factor)
    scaled_h = int(FRAME_HEIGHT * scale_factor)
    frame_img = spriteSheet.getImage(x, FRAME_WIDTH, FRAME_HEIGHT)
    frame_img = pygame.transform.scale(frame_img, (scaled_w, scaled_h))
    animationList.append(frame_img)

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

def drawText(text, fontSize, textCol, x, y):
    text_surface = get_cached_text(text, fontSize, textCol)
    game_surface.blit(text_surface, scaler.scale_pos(x,y))

def blitScaled():
    scale_x = display_width / game_width
    scale_y = display_height / game_height
    scale = min(scale_x, scale_y)

    scaled_width = int(game_width * scale)
    scaled_height = int(game_height * scale)

    x_offset = (display_width - scaled_width) // 2
    y_offset = (display_height - scaled_height) // 2

    scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_width , scaled_height))
    screen.fill((0,0,0))
    screen.blit(scaled_surface, (x_offset, y_offset))
    pygame.display.flip()

def profile_game():
    pr = cProfile.Profile()
    pr.enable()
    
    mainMenu()
    
    pr.disable()
    
    # Create a string buffer to capture the output
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    
    # Save to file
    with open('profile_results.txt', 'w') as f:
        f.write(s.getvalue())
    
    print("Profile saved to profile_results.txt")

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
    flashIndex = 0
    flashTimer = 0
    isNewHighScore = score > previousHighScore
    gameOverState = True
    while gameOverState:
        game_surface.fill((0,0,0))
        drawText("YOU CRASHED!", 40, (255,0,0), 405, 185)
        drawText(f"Your score: {score}", 20, textColor, 490, 340)
        drawText(f"High Score: {previousHighScore}", 20, textColor, 490, 360)

        if isNewHighScore:
            flashTimer +=1
            if flashTimer % 30 == 0:
                flashIndex = (flashIndex + 1) % len(c.FLASHING_COLORS)
            drawText(resultMessage, 15, c.FLASHING_COLORS[flashIndex], 350, 400)
        else:
            drawText(resultMessage, 15, textColor, 350, 400)
        
        drawText("To try again, press Start/Enter", 15, textColor, 400, 500)
        drawText("To go to the menu, press Select/Space", 15, textColor, 400, 520)
        drawText("To quit, press the Home button or Escape key", 15, textColor, 400, 540) 
        blitScaled()

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
    overlay = pygame.Surface((game_width, game_height),pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # 128 = 50% transparent
    game_surface.blit(overlay, (0, 0))
    drawText("PAUSED", 40, textColor, 525, 300)
    drawText("Press Start/Enter to resume", 20, textColor, 380, 400)
    blitScaled()
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


def playScreen(cheatEnabled = False):
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
        game_surface.fill((50,50,50))
        clock.tick(fps)
        score +=1

        currentTime = pygame.time.get_ticks()
        if currentTime - lastUpdate >= animationCooldown:
            frame +=1
            lastUpdate = currentTime
            if frame >= len(animationList):
                frame = 0
        frame_image = animationList[frame]
        x = (game_width - frame_image.get_width()) // 2
        y = (game_height - frame_image.get_height()) // 2
        game_surface.blit(frame_image, (x, y))
        drawText(f"High Score: {high_score}", 15, textColor, 1015, 430)
        drawText(f"Score: {score}", 20, textColor, 1025, 450)
        if player.isCheating:
            drawText("Power Up: INVINCIBILITY!!!", 12, textColor, 1010, 475)
        elif player.powerUpReceived is not None or player.bulletsActive:
            activePowerUp = player.powerUpReceived if player.powerUpReceived is not None else "bullets"
            drawText(f"Power Up : {activePowerUp}", 15, textColor, 1010, 475)

        if cheatEnabled:
            player.shieldActive = True
            player.bulletsActive = True
            player.isCheating = True
        #Game over cause
        if pygame.sprite.spritecollideany(player, enemy_spawner.enemy_group):
            if player.isCheating:
                pass
            elif player.shieldActive:
                player.shieldActive = False
                player.shieldSoundPlayed = False
                player.shieldCoolDownTimer = 60
            elif player.bulletsActive:
                player.bulletsActive = False
                player.shieldCoolDownTimer = 60
            elif player.shieldCoolDownTimer == 0:
                if joystick: 
                    joystick.rumble(0,1,2000)
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
            game_surface.blit(shieldSurface, shield_rect)
        
        if showHitboxes:        
            for enemy in enemy_spawner.enemy_group:
                pygame.draw.rect(game_surface, (255,0,0), enemy.rect, 2)
                pygame.draw.rect(game_surface, (0,255,0), player.rect, 2)

        action, showHitboxes = eventHandler.handle_gameplay_events(player, showHitboxes)
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "pause":
            result = pauseScreen()
            if result == "quit":
                pygame.quit()
                sys.exit()


        spriteGroup.draw(game_surface)
        spriteGroup.update()
        player.bullets.update()
        player.bullets.draw(game_surface)
        enemy_spawner.enemy_group.draw(game_surface)
        enemy_spawner.update()
        hits = pygame.sprite.groupcollide(player.bullets, enemy_spawner.enemy_group, True, True)
        if hits:
            score +=100
            hitSound.play()
            for enemy_list in hits.values():
                for enemy in enemy_list:
                    for _ in range(15):
                        particles.add(Particle(enemy.rect.center))
        itemBox_spawner.itemBox_group.draw(game_surface)
        itemBox_spawner.update()
        particles.update()
        particles.draw(game_surface)
        blitScaled()

def controlsMenu():
    pygame.display.set_caption("Controls")
    run = True
    while run:
        game_surface.fill((0,0,0))
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
        blitScaled()

def mainMenu():
    pygame.display.set_caption("Main Menu")
    pygame.mixer.music.load("assets/sounds/introSong.mp3")
    pygame.mixer.music.play()
    colorIndex = 0
    frameCounter = 0
    run = True
    cheatEnabled = False
    while run:
        game_surface.fill((0,0,255))
        clock.tick(fps)
        if cheatEnabled:
            game_surface.fill(c.FLASHING_COLORS[colorIndex])
            frameCounter +=1
            if frameCounter % 10 == 0:
                colorIndex = (colorIndex + 1) % len(c.FLASHING_COLORS)
        drawText("PERFECT RACER", 40, textColor, 380, 175)
        drawText("Press Start/Enter to begin", 20, textColor, 400, 395)
        drawText("Or press Select/Space for the controls!", 20, textColor, 265, 455)
        drawText("To quit, press the Home button or Escape key", 20, textColor, 215, 515)
        action, cheatEnabled = eventHandler.handle_main_menu_events()
        if action == "play":
            playScreen(cheatEnabled)
            return
        elif action == "controls":
            controlsMenu()
            return
        elif action == "quit":
            pygame.quit()
            sys.exit()
        blitScaled()

profile_game()
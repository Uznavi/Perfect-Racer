import pygame
import sys
import constants as c
import cProfile
import io
import pstats
import time
from scoreSystem import loadHighScore, saveHighScore
import eventHandler
import spritesheet
from playerCar import PlayerCar
from enemySpawner import EnemySpawner
from itemBoxSpawner import ItemBoxSpawner
from particles import Particle
from utilities import drawText, blitScaled

def profile_game(screen, game_surface, clock, joystick, scaler):
    pr = cProfile.Profile()
    pr.enable()
    mainMenu(screen, game_surface, clock, joystick, scaler)
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    with open('profile_results.txt', 'w') as f:
        f.write(s.getvalue())
    print("Profile saved to profile_results.txt")

def gameOverScreen(screen, game_surface, clock, joystick, scaler, score):
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
        drawText("YOU CRASHED!", 40, (255,0,0), 405, 185, game_surface, scaler)
        drawText(f"Your score: {score}", 20, c.textColor, 490, 340, game_surface, scaler)
        drawText(f"High Score: {previousHighScore}", 20, c.textColor, 490, 360, game_surface, scaler)
        if isNewHighScore:
            flashTimer +=1
            if flashTimer % 30 == 0:
                flashIndex = (flashIndex + 1) % len(c.FLASHING_COLORS)
            drawText(resultMessage, 15, c.FLASHING_COLORS[flashIndex], 350, 400, game_surface, scaler)
        else:
            drawText(resultMessage, 15, c.textColor, 350, 400, game_surface, scaler)
        drawText("To try again, press Start/Enter", 15, c.textColor, 400, 500, game_surface, scaler)
        drawText("To go to the menu, press Select/Space", 15, c.textColor, 400, 520, game_surface, scaler)
        drawText("To quit, press the Home button or Escape key", 15, c.textColor, 400, 540, game_surface, scaler)
        blitScaled(game_surface, screen, scaler)
        action = eventHandler.handle_game_over_events()
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "play":
            playScreen(screen, game_surface, clock, joystick, scaler)
            return
        elif action == "main_menu":
            mainMenu(screen, game_surface, clock, joystick, scaler)
            return

def pauseScreen(screen, game_surface, clock, joystick, scaler):
    pygame.mixer.music.load("assets/sounds/pause.ogg")
    pygame.mixer.music.play()
    paused = True
    overlay = pygame.Surface((c.game_width, c.game_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    game_surface.blit(overlay, (0, 0))
    drawText("PAUSED", 40, c.textColor, 525, 300, game_surface, scaler)
    drawText("Press Start/Enter to resume", 20, c.textColor, 380, 400, game_surface, scaler)
    drawText("To quit, press the Home button or the Escape key", 15, c.textColor, 300, 440, game_surface, scaler)
    blitScaled(game_surface, screen, scaler)
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

def playScreen(screen, game_surface, clock, joystick, scaler, cheatEnabled=False):
    pygame.display.set_caption("Game")
    pygame.mixer.music.load("assets/sounds/gameSong.mp3")
    pygame.mixer.music.play(-1)
    hitSound = pygame.mixer.Sound("assets/sounds/explosion.wav")
    imageSpriteSheet = pygame.image.load("assets/images/B i g  r o a d.png").convert_alpha()
    spriteSheet = spritesheet.SpriteSheet(imageSpriteSheet)
    animationList = []
    for x in range(c.animationLoop):
        scale_factor = (c.game_height / c.FRAME_HEIGHT) * c.HEIGHT_MULTIPLIER
        scaled_w = int(c.FRAME_WIDTH * scale_factor)
        scaled_h = int(c.FRAME_HEIGHT * scale_factor)
        frame_img = spriteSheet.getImage(x, c.FRAME_WIDTH, c.FRAME_HEIGHT)
        frame_img = pygame.transform.scale(frame_img, (scaled_w, scaled_h))
        animationList.append(frame_img)
    run = True
    lastUpdate = pygame.time.get_ticks()
    frame = 0
    score = 0
    showHitboxes = False
    high_score = loadHighScore()
    player = PlayerCar(scaler)
    enemy_spawner = EnemySpawner(scaler)
    itemBox_spawner = ItemBoxSpawner(scaler)
    particles = pygame.sprite.Group()
    spriteGroup = pygame.sprite.Group()
    spriteGroup.add(player)
    while run:
        game_surface.fill((50,50,50))
        clock.tick(c.fps)
        score +=1
        currentTime = pygame.time.get_ticks()
        if currentTime - lastUpdate >= c.animationCooldown:
            frame +=1
            lastUpdate = currentTime
            if frame >= len(animationList):
                frame = 0
        frame_image = animationList[frame]
        x = (c.game_width - frame_image.get_width()) // 2
        y = (c.game_height - frame_image.get_height()) // 2
        game_surface.blit(frame_image, (x, y))
        drawText(f"High Score: {high_score}", 14, c.textColor, 1065, 430, game_surface, scaler)
        drawText(f"Score: {score}", 15, c.textColor, 1065, 450, game_surface, scaler)
        if player.isCheating:
            drawText("Power Up: INVINCIBILITY!", 10, c.textColor, 1065, 475, game_surface, scaler)
        else:
            if player.powerUpReceived is not None or player.bulletsActive:
                activePowerUp = player.powerUpReceived if player.powerUpReceived is not None else "bullets"
                drawText(f"Power Up : {activePowerUp}", 13, c.textColor, 1065, 475, game_surface, scaler)
            if player.bulletsActive:
                drawText(f"Bullets: {player.bulletAmount}", 13, c.textColor, 1065, 490, game_surface, scaler)
            if player.shieldActive:
                drawText(f"Shield : {player.shieldRemaining}", 13, c.textColor, 1065, 490, game_surface, scaler)
        if cheatEnabled:
            player.shieldActive = True
            player.bulletsActive = True
            player.isCheating = True
        enemyHit = pygame.sprite.spritecollideany(player, enemy_spawner.enemy_group)
        if enemyHit:
            if player.isCheating:
                hitSound.play()
                for _ in range(15):
                    particles.add(Particle(enemyHit.rect.center))
                enemyHit.kill()
                score +=100
            elif player.shieldActive:
                hitSound.play()
                for _ in range(15):
                    particles.add(Particle(enemyHit.rect.center))
                enemyHit.kill()
                score +=100
            elif player.bulletsActive:
                player.bulletsActive = False
                player.shieldCoolDownTimer = 60
            elif player.shieldCoolDownTimer != 0:
                hitSound.play()
                for _ in range(15):
                    particles.add(Particle(enemyHit.rect.center))
                enemyHit.kill()
            elif player.shieldCoolDownTimer == 0:
                if joystick:
                    joystick.rumble(0,1,2000)
                gameOverScreen(screen, game_surface, clock, joystick, scaler, score)
                return
        item_box_hit = pygame.sprite.spritecollideany(player, itemBox_spawner.itemBox_group)
        if item_box_hit:
            if not player.shieldActive and not player.bulletsActive and player.powerUpReceived is None:
                player.powerUpReceived = item_box_hit.powerUp
            item_box_hit.kill()
        if player.shieldActive:
            shieldSurface = pygame.Surface((player.rect.width*2, player.rect.height*2), pygame.SRCALPHA)
            pygame.draw.ellipse(
                shieldSurface,
                (100, 200, 255, 120),
                shieldSurface.get_rect()
            )
            shield_rect = shieldSurface.get_rect(center = player.rect.center)
            game_surface.blit(shieldSurface, shield_rect)
        if player.shieldActive and not player.isCheating:
            secondsElapsed = int(time.time()) - player.shieldStartTime
            player.shieldRemaining = max(0, player.shieldTimer - secondsElapsed)
            if player.shieldRemaining <= 0:
                player.shieldActive = False
                player.shieldSoundPlayed = False
                player.powerUpReceived = None
                player.shieldCoolDownTimer = 60
        if showHitboxes:
            for enemy in enemy_spawner.enemy_group:
                pygame.draw.rect(game_surface, (255,0,0), enemy.rect, 2)
                pygame.draw.rect(game_surface, (0,255,0), player.rect, 2)
        action, showHitboxes = eventHandler.handle_gameplay_events(player, showHitboxes)
        if action == "pause":
            pauseStartTime = time.time()
            result = pauseScreen(screen, game_surface, clock, joystick, scaler)
            pauseEndTime = time.time()
            pausedDuration = int(pauseEndTime - pauseStartTime)
            if result == "resume" and player.shieldActive and player.shieldRemaining is not None:
                player.shieldStartTime += pausedDuration
            if result == "quit":
                pygame.quit()
                sys.exit()
        elif action == "bomb" and player.powerUpReceived == "bomb":
            carsHit = len(enemy_spawner.enemy_group)
            for enemy in enemy_spawner.enemy_group:
                hitSound.play()
                for _ in range(15):
                    particles.add(Particle(enemy.rect.center))
                enemy.kill()
            score += carsHit * 100
            player.powerUpReceived = None
        spriteGroup.update()
        spriteGroup.draw(game_surface)
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
        blitScaled(game_surface, screen, scaler)

def controlsMenu(screen, game_surface, clock, joystick, scaler):
    pygame.display.set_caption("Controls")
    run = True
    while run:
        game_surface.fill((0,0,0))
        clock.tick(c.fps)
        drawText("CONTROLS", 40, c.textColor, 495, 125, game_surface, scaler)
        drawText("D-Pad / WASD: Directional Movement (Up, Down, Left, Right)", 20, c.textColor, 70, 350, game_surface, scaler)
        drawText("Y/Square: Power-Up (Can only be used when in inventory)", 20, c.textColor, 100, 395, game_surface, scaler)
        drawText("This game supports PS5 DualSense and Switch Pro Controller", 15, c.textColor, 210, 450, game_surface, scaler)
        drawText("Press Select/Space again to go back to the title screen", 10, c.textColor, 370, 500, game_surface, scaler)
        action = eventHandler.handle_controls_screen_events()
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "main_menu":
            mainMenu(screen, game_surface, clock, joystick, scaler)
            return
        blitScaled(game_surface, screen, scaler)

def mainMenu(screen, game_surface, clock, joystick, scaler):
    pygame.display.set_caption("Main Menu")
    pygame.mixer.music.load("assets/sounds/introSong.mp3")
    pygame.mixer.music.play()
    colorIndex = 0
    frameCounter = 0
    run = True
    cheatEnabled = False
    while run:
        game_surface.fill((0,0,255))
        clock.tick(c.fps)
        if cheatEnabled:
            game_surface.fill(c.FLASHING_COLORS[colorIndex])
            frameCounter +=1
            if frameCounter % 10 == 0:
                colorIndex = (colorIndex + 1) % len(c.FLASHING_COLORS)
        drawText("PERFECT RACER", 40, c.textColor, 380, 175, game_surface, scaler)
        drawText("Press Start/Enter to begin", 20, c.textColor, 400, 395, game_surface, scaler)
        drawText("Or press Select/Space for the controls!", 20, c.textColor, 265, 455, game_surface, scaler)
        drawText("To quit, press the Home button or Escape key", 20, c.textColor, 215, 515, game_surface, scaler)
        action, cheatEnabled = eventHandler.handle_main_menu_events()
        if action == "play":
            playScreen(screen, game_surface, clock, joystick, scaler, cheatEnabled)
            return
        elif action == "controls":
            controlsMenu(screen, game_surface, clock, joystick, scaler)
            return
        elif action == "quit":
            pygame.quit()
            sys.exit()
        blitScaled(game_surface, screen, scaler)
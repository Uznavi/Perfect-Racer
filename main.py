import pygame, sys
import spritesheet
from playerCar import PlayerCar
from enemySpawner import EnemySpawner
from itemBoxSpawner import ItemBoxSpawner
#TODO : At the end, clean up the main file and add stuff to other files, like constants and stuff
pygame.init()
pygame.mixer.init()

fps = 60
clock = pygame.time.Clock()

#For now I'll keep these guys here, after the initial playtesting I'll decide to bring them back
#That being said if I need to bring them back, then I'll have to scale it all over again, fml
#HEY YOU! PLAYTESTER! JUST LIKE IT THIS WAY, PLEASE
#P.S. why are you reading this? you fucking nerd ☝️🤓

#Screen constants
# screenWidth = 1300
# screenHeight = 645
# screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#Sprite Sheet Information and Text Color
imageSpriteSheet = pygame.image.load("assets/images/B i g  r o a d.png").convert_alpha()
spriteSheet = spritesheet.SpriteSheet(imageSpriteSheet)
textColor = (255,255,255)
#Animation process
animationList = []
animationLoop = 5
animationCooldown = 10

for x in range(animationLoop):
    animationList.append(spriteSheet.getImage(x, 100, 100, 7.15))

#Text function
#TODO: At some point, make a constant x and y variable to not add a new one every time
def drawText(text, fontSize, textCol, x, y):
    font = pygame.font.Font("assets/font/PressStart2P.ttf", fontSize)
    text_surface = font.render(text, True, textCol)
    screen.blit(text_surface, (x,y))
#Screen Event Handlers

def gameOverScreen(score):
    pygame.mixer.music.load("assets/sounds/gameOverSong.mp3")
    pygame.mixer.music.play()
    gameOverState = True
    while gameOverState:
        screen.fill((0,0,0))
        drawText("YOU CRASHED!", 40, (255,0,0), 405, 185)
        drawText(f"Your score: {score}", 20, textColor, 490, 340)
        drawText("To try again, press Start/Enter", 15, textColor, 400, 600)
        drawText("To go to the menu, press Select/Space", 15, textColor, 400, 620)
        drawText("To quit, press the Home button or Escape key", 15, textColor, 400, 640)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    gameOverState = False
                    playScreen()
                if event.key == pygame.K_SPACE:
                    mainMenu()
        pygame.display.update()


def pauseScreen():
    # During the playtest, ask to see if they mind the pause music. It's just that I wanted the game song to resume from where it left 
    #off when paused but apparently that can't be done so just ask everyone how they feel about it and if the pause song should stay
    pygame.mixer.music.load("assets/sounds/pause.mp3")
    pygame.mixer.music.play(-1)
    paused = True

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0,0,0,128))

    screen.blit(overlay, (0,0))
    drawText("PAUSED", 40, textColor, 525, 300)
    drawText("Press Start/Enter to resume", 20, textColor, 380, 400)
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    paused = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/sounds/gameSong.mp3")
                    pygame.mixer.music.play(-1)
        clock.tick(10)


def playScreen():
    #TODO: Since this is the meat and bones of the game, try to make it clearer what is an object and what is the object update function
    pygame.display.set_caption("Game")
    pygame.mixer.music.load("assets/sounds/gameSong.mp3")
    pygame.mixer.music.play(-1)
    run = True
    lastUpdate = pygame.time.get_ticks()
    frame = 0
    score = 0
    showHitboxes = False

    #Game objects
    player = PlayerCar()
    enemy_spawner = EnemySpawner()
    itemBox_spawner = ItemBoxSpawner()
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
        drawText(f"Score: {score}", 20, textColor, 1025, 450)

        if pygame.sprite.spritecollideany(player, enemy_spawner.enemy_group):
            gameOverScreen(score)
        
        if showHitboxes:        
            for enemy in enemy_spawner.enemy_group:
                pygame.draw.rect(screen, (255,0,0), enemy.rect, 2)
                pygame.draw.rect(screen, (0,255,0), player.rect, 2)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pauseScreen()
                if event.key == pygame.K_a:
                    player.vel_x = -player.speed
                if event.key == pygame.K_d:
                    player.vel_x = player.speed
                if event.key == pygame.K_w:
                    player.vel_y = -player.speed
                if event.key == pygame.K_s:
                    player.vel_y = player.speed
                if event.key == pygame.K_h: #SUPER COOL AND EPIC DEBUGGING KEY THAT ALLOWS YOU TO SEE
                    showHitboxes = not showHitboxes #THE FUCKING HITBOXES
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.vel_x = 0
                if event.key == pygame.K_d:
                    player.vel_x = 0
                if event.key == pygame.K_w:
                    player.vel_y = 0
                if event.key == pygame.K_s:
                    player.vel_y = 0
        spriteGroup.draw(screen)
        spriteGroup.update()
        enemy_spawner.enemy_group.draw(screen)
        enemy_spawner.update()
        itemBox_spawner.itemBox_group.draw(screen)
        itemBox_spawner.update()
        pygame.display.update()

def controlsMenu():
    pygame.display.set_caption("Controls")
    run = True
    while run:
        screen.fill((0,0,0))
        clock.tick(fps)
        drawText("CONTROLS", 40, textColor, 470, 125)
        drawText("D-Pad / WASD: Directional Movement (Up, Down, Left, Right)", 20, textColor, 70, 350)
        drawText("Y: Power-Up (Can only be used when in inventory)", 20, textColor, 165, 395)
        drawText("Press Select/Space again to go back to the title screen", 10, textColor, 370, 500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mainMenu()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def mainMenu():
    pygame.display.set_caption("Main Menu")
    # Load and play music once at the start
    pygame.mixer.music.load("assets/sounds/intro.mp3")
    pygame.mixer.music.play()
    run = True
    while run:
        clock.tick(fps)
        screen.fill((0,0,255))
        drawText("PERFECT RACER", 40, textColor, 375, 200)
        drawText("Press Start/Enter to begin", 20, textColor, 400, 450)
        drawText("Or press Select/Space for the controls!", 20, textColor, 295, 495)
        drawText("To quit, press the Home button or Escape key", 20, textColor, 250, 545)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    playScreen()
                if event.key == pygame.K_SPACE:
                    controlsMenu()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

mainMenu()
import pygame, sys
import spritesheet
from playerCar import PlayerCar
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
player = PlayerCar()
spriteGroup = pygame.sprite.Group()
spriteGroup.add(player)

for x in range(animationLoop):
    animationList.append(spriteSheet.getImage(x, 100, 100, 7.18))

#Text function
def drawText(text, fontSize, textCol, x, y):
    font = pygame.font.Font("assets/font/PressStart2P.ttf", fontSize)
    text_surface = font.render(text, True, textCol)
    screen.blit(text_surface, (x,y))
#Screen Event Handlers
def playScreen():
    pygame.display.set_caption("Game")
    pygame.mixer.music.load("assets/sounds/gameSong.mp3")
    pygame.mixer.music.play(-1)
    run = True
    lastUpdate = pygame.time.get_ticks()
    frame = 0
    score = 0

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

        screen.blit(animationList[frame], (300,0))
        drawText(f"Score: {score}", 20, textColor, 1025, 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.vel_x = -player.speed
                if event.key == pygame.K_d:
                    player.vel_x = player.speed
                if event.key == pygame.K_w:
                    player.vel_y = -player.speed
                if event.key == pygame.K_s:
                    player.vel_y = player.speed
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
        # spriteGroup.draw(screen)
        pygame.display.update()

def controlsMenu():
    pygame.display.set_caption("Controls")
    run = True
    while run:
        screen.fill((0,0,0))
        clock.tick(fps)
        drawText("CONTROLS", 40, textColor, 470, 125)
        drawText("D-Pad: Directional Movement (Up, Down, Left, Right)", 20, textColor, 135, 350)
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
        drawText("Press Start to begin", 20, textColor, 415, 450)
        drawText("Or press Select for the controls!", 20, textColor, 315, 495)
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
import pygame, sys

pygame.init()
pygame.mixer.init()

screenWidth = 1300
screenHeight = 645
screen = pygame.display.set_mode((screenWidth, screenHeight))


# font = pygame.font.Font("PressStart2P.ttf")
textColor = (255,255,255)

def drawText(text, fontSize, textCol, x, y):
    font = pygame.font.Font("PressStart2P.ttf", fontSize)
    text_surface = font.render(text, True, textCol)
    screen.blit(text_surface, (x,y))

def controlsMenu():
    pygame.display.set_caption("Controls")
    run = True
    while run:
        screen.fill((0,0,0))
        drawText("CONTROLS", 40, textColor, 500, 125)
        drawText("D-Pad: Directional Movement (Up, Down, Left, Right)", 20, textColor, 175, 350)
        drawText("Y: Power-Up (Can only be used when in inventory)", 20, textColor, 200, 395)
        drawText("Press Select/Space again to go back to the title screen", 10, textColor, 400, 500)
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
    pygame.mixer.music.load("intro.mp3")
    pygame.mixer.music.play()
    run = True
    while run:
        screen.fill((0,0,255))
        drawText("PERFECT RACER", 40, textColor, 400, 125)
        drawText("Press Start to begin", 20, textColor, 435, 350)
        drawText("Or press Select for the controls!", 20, textColor, 340, 395)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controlsMenu()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

mainMenu()
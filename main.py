import pygame, sys

pygame.init()

screenWidth = 1300
screenHeight = 645
screen = pygame.display.set_mode((screenWidth, screenHeight))


font = pygame.font.Font("PressStart2P.ttf", 40)
textColor = (255,255,255)

def drawText(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def mainMenu():
    pygame.display.set_caption("Main Menu")
    run = True
    while run:
    
        screen.fill((0,0,255))
        drawText("PERFECT RACER", font, textColor, 400, 125)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()
mainMenu()
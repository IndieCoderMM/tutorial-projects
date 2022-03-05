import random
import sys
import time
import pygame
from pygame.locals import *

FPS = 30
WINWIDTH = 640
WINHEIGHT = 480
FLASHSPD = 500
FLASHDLY = 200
BTNSIZE = 200
BTNGAP = 20
TIMEOUT = 4

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

XMARGIN = int((WINWIDTH - (2 * BTNSIZE) - BTNGAP) / 2)
YMARGIN = int((WINHEIGHT - (2 * BTNSIZE) - BTNGAP) / 2)

# Rect objects for each button
YRECT = pygame.Rect(XMARGIN, YMARGIN, BTNSIZE, BTNSIZE)
BRECT = pygame.Rect(XMARGIN + BTNSIZE + BTNGAP, YMARGIN, BTNSIZE, BTNSIZE)
RRECT = pygame.Rect(XMARGIN, YMARGIN + BTNSIZE + BTNGAP, BTNSIZE, BTNSIZE)
GRECT = pygame.Rect(XMARGIN + BTNSIZE + BTNGAP, YMARGIN + BTNSIZE + BTNGAP, BTNSIZE, BTNSIZE)


def main():
    global FPSCLK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Simulate')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q W A S keys.', 1, WHITE)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINHEIGHT - 25)

    # Loading the sound files
    # BEEP1 = pygame.mixer.Sound('beep1.')

    pattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0

    waitingForInput = False

    while True:
        clickedButton = None
        DISPLAYSURF.fill(BGCOLOR)
        draw_buttons()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        check_for_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = get_btn_clicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN

        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flash_btn_animation(button)
                pygame.time.wait(FLASHDLY)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                flash_btn_animation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    change_bg_animation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0
            elif (clickedButton and clickedButton != pattern[currentStep]) or \
                    (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                game_over_animation()
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                change_bg_animation()
            pygame.display.update()
            FPSCLK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def flash_btn_animation(color, animationSpd=50):
    if color == YELLOW:
        # sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YRECT
    elif color == BLUE:
        # sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BRECT
    elif color == RED:
        # sound = BEEP2
        flashColor = BRIGHTRED
        rectangle = RRECT
    elif color == GREEN:
        # sound = BEEP2
        flashColor = BRIGHTGREEN
        rectangle = GRECT
    orgSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BTNSIZE, BTNSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    # sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):  # Animation Loop
        # In first iteration start=0 end=255 step=1 & in second start=255 end=0 step=-1
        for alpha in range(start, end, animationSpd * step):
            check_for_quit()
            DISPLAYSURF.blit(orgSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLK.tick(FPS)
    DISPLAYSURF.blit(orgSurf, (0, 0))

def draw_buttons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YRECT)
    pygame.draw.rect(DISPLAYSURF, WHITE, (XMARGIN - 1, YMARGIN - 1, BTNSIZE + 1, BTNSIZE + 1), 2)
    pygame.draw.rect(DISPLAYSURF, BLUE, BRECT)
    pygame.draw.rect(DISPLAYSURF, WHITE, (XMARGIN + BTNSIZE + BTNGAP - 1, YMARGIN - 1, BTNSIZE + 1, BTNSIZE + 1), 2)
    pygame.draw.rect(DISPLAYSURF, RED, RRECT)
    pygame.draw.rect(DISPLAYSURF, WHITE, (XMARGIN - 1, YMARGIN + BTNSIZE + BTNGAP - 1, BTNSIZE + 1, BTNSIZE + 1), 2)
    pygame.draw.rect(DISPLAYSURF, GREEN, GRECT)
    pygame.draw.rect(DISPLAYSURF, WHITE, (XMARGIN + BTNSIZE + BTNGAP - 1, YMARGIN + BTNSIZE + BTNGAP - 1, BTNSIZE + 1, BTNSIZE + 1), 2)


def change_bg_animation(animationSpd=40):
    global BGCOLOR
    newBgcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    newBgsurf = pygame.Surface((WINWIDTH, WINHEIGHT))
    newBgsurf = newBgsurf.convert_alpha()
    r, g, b = newBgcolor
    for alpha in range(0, 255, animationSpd):
        check_for_quit()
        DISPLAYSURF.fill(BGCOLOR)
        newBgsurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgsurf, (0, 0))

        draw_buttons()

        pygame.display.update()
        FPSCLK.tick(FPS)
    BGCOLOR = newBgcolor


def game_over_animation(color=WHITE, animationSpd=50):
    orgSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    r, g, b = color
    for i in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpd * step):
                check_for_quit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(orgSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                draw_buttons()
                pygame.display.update()
                FPSCLK.tick(FPS)


def get_btn_clicked(x, y):
    if YRECT.collidepoint((x, y)):
        return YELLOW
    elif BRECT.collidepoint((x, y)):
        return BLUE
    elif RRECT.collidepoint((x, y)):
        return RED
    elif GRECT.collidepoint((x, y)):
        return GREEN
    return None


if __name__ == '__main__':
    main()

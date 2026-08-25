import pygame,sys,random
pygame.init()
screen = pygame.display.set_mode()
running = True
LCTRL = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                LCTRL = True
            if event.key == pygame.K_ESCAPE and LCTRL:
                running = False
        if event.type == pygame.KEYUP:
            if event.type == pygame.K_LSHIFT:
                LCTRL = False
#Kevin test 입니다.
#megiddo test 입니다.
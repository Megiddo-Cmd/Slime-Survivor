import pygame,sys,random
pygame.init()
info = pygame.display.Info()
width = info.current_w
height = info.current_h
screen = pygame.display.set_mode()

# 맥은 \\가 아니라 /로 해야함 분기 처리 부탁
i_s_b = pygame.image.load('src\\img\\slime_back.png')
i_s_b = pygame.transform.scale(i_s_b,(50,50))
i_s_f = pygame.image.load('src\\img\\slime_front.png')
i_s_f = pygame.transform.scale(i_s_f,(50,50))
i_s_l = pygame.image.load('src\\img\\slime_lr.png')
i_s_l = pygame.transform.scale(i_s_l,(50,50))
i_s_r = pygame.transform.flip(i_s_l,1,0)
 
p_rect = pygame.Rect(0,0,50,50)
p_i = i_s_f
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
    keyInput = pygame.key.get_pressed()
    if keyInput[pygame.K_LEFT] and p_rect.left > 0:
        p_rect.left -= 2
        p_i = i_s_l
    if keyInput[pygame.K_RIGHT] and p_rect.right < width:
        p_rect.left += 2
        p_i = i_s_r
    if keyInput[pygame.K_UP] and p_rect.top > 0:
        p_rect.top -= 2
        p_i = i_s_f
    if keyInput[pygame.K_DOWN] and p_rect.bottom < height:
        p_rect.top += 2
        p_i = i_s_b
    screen.fill((0,0,0))
    screen.blit(p_i,p_rect)
    pygame.display.update()
#Kevin test 입니다.
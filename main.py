import pygame,sys,random,os
pygame.init()
info = pygame.display.Info()
width = info.current_w
height = info.current_h
screen = pygame.display.set_mode()

#경로지정
path_back = os.path.join("src", "img", "slime_back.png")
path_front = os.path.join("src", "img", "slime_front.png")
path_lr = os.path.join("src", "img", "slime_lr.png")
path_back_lr = os.path.join("src", "img", "slime_back_lr.png")

#후방
i_s_b = pygame.image.load(path_back)
i_s_b = pygame.transform.scale(i_s_b,(50,50))
#전방
i_s_f = pygame.image.load(path_front)
i_s_f = pygame.transform.scale(i_s_f,(50,50))
#좌우
i_s_l = pygame.image.load(path_lr)
i_s_l = pygame.transform.scale(i_s_l,(50,50))
i_s_r = pygame.transform.flip(i_s_l,1,0)
#후방 좌우
i_s_bl = pygame.image.load(path_back_lr)
i_s_bl = pygame.transform.scale(i_s_bl, (50, 50))
i_s_br = pygame.transform.flip(i_s_bl, 1, 0)

#후방좌우 이미지를 아래쪽 화살표와 좌/우 화살표를 동시에 눌렀을 때 사용하도록 설정 필요 - Megiddo-Cmd가 완료

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
        if keyInput[pygame.K_LEFT] and p_rect.left > 0:
            p_i = i_s_bl
        if keyInput[pygame.K_RIGHT] and p_rect.right < width:
            p_i = i_s_br
    screen.fill((255,255,255))
    screen.blit(p_i,p_rect)
    pygame.display.update()
#Kevin test 입니다.
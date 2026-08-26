import pygame,sys,random,os
pygame.init()
info = pygame.display.Info()
width = info.current_w
height = info.current_h
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Slime Survivor")
pygame.display.set_icon(pygame.image.load(os.path.join(".","Icon.png")))

#경로지정
path_back = os.path.join("src", "img", "player", "slime_back.png")
path_front = os.path.join("src", "img", "player", "slime_front.png")
path_lr = os.path.join("src", "img", "player", "slime_lr.png")
path_back_lr = os.path.join("src", "img", "player", "slime_back_lr.png")
path_stage1_1 = os.path.join("src", "img", "stage1", "stage1_1.png")
path_stage1_2 = os.path.join("src", "img", "stage1", "stage1_2.png")

player_size = 70
player_speed = 8

#후방
i_s_b = pygame.image.load(path_back)
i_s_b = pygame.transform.scale(i_s_b,(player_size,player_size))
#전방
i_s_f = pygame.image.load(path_front)
i_s_f = pygame.transform.scale(i_s_f,(player_size,player_size))
#좌우
i_s_l = pygame.image.load(path_lr)
i_s_l = pygame.transform.scale(i_s_l,(player_size,player_size))
i_s_r = pygame.transform.flip(i_s_l,1,0)
#후방 좌우
i_s_bl = pygame.image.load(path_back_lr)
i_s_bl = pygame.transform.scale(i_s_bl, (player_size, player_size))
i_s_br = pygame.transform.flip(i_s_bl, 1, 0)
TILE_SIZE = (128, 128)

stage1_images = [
    pygame.transform.scale(pygame.image.load(path_stage1_1), TILE_SIZE),
    pygame.transform.scale(pygame.image.load(path_stage1_2), TILE_SIZE)
]

#후방좌우 이미지를 아래쪽 화살표와 좌/우 화살표를 동시에 눌렀을 때 사용하도록 설정 필요 - Megiddo-Cmd가 완료

p_rect = pygame.Rect(width // 2, height // 2, player_size, player_size)
p_i = i_s_f
running = True
LCTRL = False

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                LCTRL = True
            if event.key == pygame.K_ESCAPE and LCTRL:
                running = False
        if event.type == pygame.KEYUP:
            if event.type == pygame.K_LSHIFT:
                LCTRL = False

    keyInput = pygame.key.get_pressed()
    if keyInput[pygame.K_LEFT]:
        p_rect.left -= player_speed
        p_i = i_s_l
    if keyInput[pygame.K_RIGHT]:
        p_rect.left += player_speed
        p_i = i_s_r
    if keyInput[pygame.K_UP]:
        p_rect.top -= player_speed
        p_i = i_s_f
    if keyInput[pygame.K_DOWN]:
        p_rect.top += player_speed
        p_i = i_s_b
        if keyInput[pygame.K_LEFT]:
            p_i = i_s_bl
        elif keyInput[pygame.K_RIGHT]:
            p_i = i_s_br

    screen.fill((255,255,255))

    cam_x = p_rect.centerx - width // 2
    cam_y = p_rect.centery - height // 2
    chunk_size = TILE_SIZE[0] * 2  # 128 * 2 = 256 (쿼드블록 전체 가로/세로 크기)
    
    start_x = -(p_rect.x % chunk_size)
    start_y = -(p_rect.y % chunk_size)

    for bx in range(start_x - chunk_size, width + chunk_size, chunk_size):
        for by in range(start_y - chunk_size, height + chunk_size, chunk_size):
            # 2개의 타일(stage1_images[0], stage1_images[1])을 2x2 쿼드블록으로 배치
            # 예시 구조 (랜덤 섞임에 따라 2x2 형태가 쿼드블록 단위로 반복됨):
            screen.blit(stage1_images[0], (bx, by))                               # 좌상단 (1행 1열)
            screen.blit(stage1_images[1], (bx + TILE_SIZE[0], by))                # 우상단 (1행 2열)
            screen.blit(stage1_images[1], (bx, by + TILE_SIZE[1]))                # 좌하단 (2행 1열)
            screen.blit(stage1_images[0], (bx + TILE_SIZE[0], by + TILE_SIZE[1])) # 우하단 (2행 2열)

    player_screen_pos = (width // 2 - 25, height // 2 - 25)
    screen.blit(p_i, player_screen_pos)

    pygame.display.update()
    clock.tick(60)
#Kevin test 입니다.
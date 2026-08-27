import pygame, sys, random, os, math
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
path_skill_q = os.path.join("src", "img", "player", "slime_skill_q.png")

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

skill_q_image = pygame.image.load(path_skill_q)
skill_q_image = pygame.transform.scale(skill_q_image, (40, 40))  # 스킬 이미지 크기 조정

TILE_SIZE = (128, 128)

stage1_images = [
    pygame.transform.scale(pygame.image.load(path_stage1_1), TILE_SIZE),
    pygame.transform.scale(pygame.image.load(path_stage1_2), TILE_SIZE)
]

max_hp = 100
player_hp = max_hp
hit_cooldown = 0  
defense_buff = 0  # R: 신체장갑 버프 지속 시간

# 스킬 발사체 (점강사 등) 관리 리스트
projectiles = []

class Projectile:
    def __init__(self, x, y, target_x, target_y):
        self.size = 60
        base_img = pygame.transform.scale(skill_q_image, (self.size, self.size))
        
        # 각도 계산 (라디안 -> 각도 변환)
        self.angle = math.atan2(target_y - y, target_x - x)
        degrees = math.degrees(self.angle)
        
        # 참격 이미지의 기본 방향에 맞게 회전 각도를 보정합니다.
        # 만약 이래도 방향이 이상하면 -90도나 +90도 등으로 숫자를 조절해 보면 딱 맞습니다!
        self.image = pygame.transform.rotate(base_img, -degrees - 110)
        self.rect = self.image.get_rect(center=(x, y))
        
        speed = 16
        self.dx = math.cos(self.angle) * speed
        self.dy = math.sin(self.angle) * speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy






p_rect = pygame.Rect(width // 2, height // 2, player_size, player_size)
p_i = i_s_f
running = True
LCTRL = False

clock = pygame.time.Clock()

class Enemy:
    def __init__(self, x, y):
        self.hp = 30
        self.size = 50
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.speed = 4
        self.color = (200, 50, 50)

    def move(self, target_rect):
        if self.rect.x < target_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target_rect.x:
            self.rect.x -= self.speed

        if self.rect.y < target_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target_rect.y:
            self.rect.y -= self.speed

enemies = []
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1500)

last_dir_x, last_dir_y = 0, 1

while running:
    if hit_cooldown > 0:
        hit_cooldown -= 1
    if defense_buff > 0:
        defense_buff -= 1

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
            
            # 스킬 입력을 KEYDOWN 이벤트 안으로 이동하여 연사 방지
            if event.key == pygame.K_q:
                print("스킬 발동: 수인 발사!")
                target_x, target_y = 0, 0
                if enemies:
                    # 가장 가까운 적을 자동 조준
                    closest_enemy = min(enemies, key=lambda e: math.hypot(e.rect.centerx - p_rect.centerx, e.rect.centery - p_rect.centery))
                    target_x, target_y = closest_enemy.rect.centerx, closest_enemy.rect.centery
                else:
                    # 적이 없으면 마지막 이동 방향으로 발사
                    target_x, target_y = p_rect.centerx + last_dir_x * 100, p_rect.centery + last_dir_y * 100
                
                projectiles.append(Projectile(p_rect.centerx, p_rect.centery, target_x, target_y))


            if event.key == pygame.K_w:
                # W: 점강사 (실 발사 및 자동 조준)
                print("스킬 발동: 점강사!")
                #추후 구현

            if event.key == pygame.K_e:
                # E: 마비톡식 (넓은 범위의 적에게 데미지)
                print("스킬 발동: 마비톡식!")
                for enemy in enemies[:]:
                    if abs(p_rect.centerx - enemy.rect.centerx) < 250 and abs(p_rect.centery - enemy.rect.centery) < 250:
                        enemy.hp -= 25
                        if enemy.hp <= 0:
                            enemies.remove(enemy)

            if event.key == pygame.K_r:
                # R: 신체장갑 (방어력 버프 부여)
                print("스킬 발동: 신체장갑!")
                defense_buff = 180  # 약 3초간 버프

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                LCTRL = False
        
        if event.type == SPAWN_ENEMY:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                ex = random.randint(p_rect.x - width, p_rect.x + width)
                ey = p_rect.y - height // 2 - 100
            elif side == 'bottom':
                ex = random.randint(p_rect.x - width, p_rect.x + width)
                ey = p_rect.y + height // 2 + 100
            elif side == 'left':
                ex = p_rect.x - width // 2 - 100
                ey = random.randint(p_rect.y - height, p_rect.y + height)
            else:
                ex = p_rect.x + width // 2 + 100
                ey = random.randint(p_rect.y - height, p_rect.y + height)
            
            enemies.append(Enemy(ex, ey))
    

    keyInput = pygame.key.get_pressed()
    
    # 이동 방향 체크 및 마지막 방향 기록
    move_x, move_y = 0, 0
    if keyInput[pygame.K_LEFT]:
        move_x = -1
        p_rect.left -= player_speed
        p_i = i_s_l
    if keyInput[pygame.K_RIGHT]:
        move_x = 1
        p_rect.left += player_speed
        p_i = i_s_r
    if keyInput[pygame.K_UP]:
        move_y = -1
        p_rect.top -= player_speed
        p_i = i_s_f
    if keyInput[pygame.K_DOWN]:
        move_y = 1
        p_rect.top += player_speed
        p_i = i_s_b
        if keyInput[pygame.K_LEFT]:
            p_i = i_s_bl
        elif keyInput[pygame.K_RIGHT]:
            p_i = i_s_br
            
    if move_x != 0 or move_y != 0:
        last_dir_x, last_dir_y = move_x, move_y

    for proj in projectiles[:]:
        proj.update()
        hit_proj = False
        for enemy in enemies[:]:
            if proj.rect.colliderect(enemy.rect):
                # 명중한 적과 주변 적들에게 실 압박 폭발 데미지 부여!
                for target in enemies[:]:
                    # 폭발 반경(예: 80픽셀) 내의 적들에게 광역 데미지
                    if math.hypot(target.rect.centerx - proj.rect.centerx, target.rect.centery - proj.rect.centery) < 80:
                        target.hp -= 50  # 강력한 폭발 데미지
                        if target.hp <= 0 and target in enemies:
                            enemies.remove(target)
                hit_proj = True
                break
        
        # 화면 밖을 벗어나거나 적중하면 제거
        if hit_proj or abs(proj.rect.x - p_rect.x) > width or abs(proj.rect.y - p_rect.y) > height:
            if proj in projectiles:
                projectiles.remove(proj)

    for enemy in enemies[:]:
        enemy.move(p_rect)
        if p_rect.colliderect(enemy.rect):
            if hit_cooldown == 0:
                damage = 10 if defense_buff > 0 else 20  # 신체장갑 켜져있으면 데미지 경감
                player_hp -= damage  
                hit_cooldown = 30  
                print(f"Hit! Current HP: {player_hp}")
                if player_hp <= 0:
                    print("Game Over!")
                    running = False

    screen.fill((255,255,255))

    cam_x = p_rect.centerx - width // 2
    cam_y = p_rect.centery - height // 2
    chunk_size = TILE_SIZE[0] * 2  
    
    start_x = -(p_rect.x % chunk_size)
    start_y = -(p_rect.y % chunk_size)

    for bx in range(start_x - chunk_size, width + chunk_size, chunk_size):
        for by in range(start_y - chunk_size, height + chunk_size, chunk_size):
            screen.blit(stage1_images[0], (bx, by))                               
            screen.blit(stage1_images[1], (bx + TILE_SIZE[0], by))                
            screen.blit(stage1_images[1], (bx, by + TILE_SIZE[1]))                
            screen.blit(stage1_images[0], (bx + TILE_SIZE[0], by + TILE_SIZE[1])) 

    for enemy in enemies:
        draw_x = enemy.rect.x - p_rect.x + (width // 2 - player_size // 2)
        draw_y = enemy.rect.y - p_rect.y + (height // 2 - player_size // 2)
        pygame.draw.rect(screen, enemy.color, (draw_x, draw_y, enemy.size, enemy.size))

    # 투사체 렌더링
    for proj in projectiles:
        draw_x = proj.rect.x - p_rect.x + (width // 2 - player_size // 2)
        draw_y = proj.rect.y - p_rect.y + (height // 2 - player_size // 2)
        screen.blit(proj.image, (draw_x, draw_y))

    player_screen_pos = (width // 2 - player_size // 2, height // 2 - player_size // 2)
    
    # 무적 시간 동안 플레이어가 깜빡이도록 연출
    if hit_cooldown == 0 or (hit_cooldown // 5) % 2 == 0:
        screen.blit(p_i, player_screen_pos)

    # --- 플레이어 크기에 맞춘 중앙 정렬 체력바 UI ---
    bar_width = player_size  # 플레이어 크기(70)와 동일하게 설정
    bar_height = 8
    bar_x = width // 2 - bar_width // 2
    bar_y = height // 2 - player_size // 2 - 15
    
    # 체력바 배경 (회색)
    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    # 현재 체력 (초록색)
    current_bar_width = int(bar_width * (player_hp / max_hp))
    if current_bar_width > 0:
        pygame.draw.rect(screen, (50, 200, 50), (bar_x, bar_y, current_bar_width, bar_height))
    # 체력바 테두리 (검은색)
    pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    # 신체장갑(R) 버프 활성화 시 플레이어 주변 이펙트
    if defense_buff > 0:
        pygame.draw.circle(screen, (100, 150, 255), (width // 2, height // 2), player_size // 2 + 10, 2)

    pygame.display.update()
    clock.tick(60)

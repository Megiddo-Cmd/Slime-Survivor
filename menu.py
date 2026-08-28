import platform
import pygame
import sys
import os

def get_custom_font(size, bold=False):
    # 프로젝트 내 폰트 파일 경로 지정 (예: src/font/CustomFont.ttf)
    font_path = os.path.join("src", "font", "notosans.ttf")
    
    try:
        # 파일이 존재하면 해당 폰트 로드
        return pygame.font.Font(font_path, size)
    except FileNotFoundError:
        # 파일이 없을 경우 시스템 기본 폰트로 안전하게 폴백
        print(f"경고: 폰트 파일을 찾을 수 없습니다 ({font_path}). 기본 폰트를 사용합니다.")
        return pygame.font.SysFont("Arial", size, bold=bold)


def run_menu():
    pygame.init()
    width, height = 800, 700
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Slime Survivor - Menu")
    clock = pygame.time.Clock()

    # 폰트 설정 (시스템 기본 폰트 사용)
    font_title = get_custom_font(50)
    font_sub = get_custom_font(30)
    font_btn = get_custom_font(40)

    # 스테이지 정보 데이터
    stages = [
        {"title": "1. 시작의 동굴", "img_path": os.path.join("src", "img", "stage1", "stage1_Cover.png")},
        # 나중에 스테이지 2, 3 등은 여기에 추가하면 됩니다!
    ]
    current_stage_idx = 0

    # 스테이지 대표 이미지 로드 함수
    def load_stage_image(path):
        try:
            img = pygame.image.load(path)
            return pygame.transform.scale(img, (260, 260)) # 1:1 정방형 사이즈
        except:
            # 이미지가 없을 경우 대체용 서피스 생성
            surf = pygame.Surface((260, 260))
            surf.fill((100, 150, 100))
            return surf

    stage_image = load_stage_image(stages[current_stage_idx]["img_path"])

    while True:
        # 화면 크기 동적 대응
        w, h = screen.get_size()
        
        # 배경 채우기 (차가운 다이아/얼음 계열 다크 네이비)
        screen.fill((20, 24, 38))

        # 1. 스테이지 제목 렌더링
        title_text = stages[current_stage_idx]["title"]
        title_surf = font_title.render(title_text, True, (180, 230, 255))
        screen.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 80))

        # 2. 스테이지 대표 1:1 이미지 렌더링 (중앙 배치)
        img_x = w // 2 - 130
        img_y = 150
        
        # 이미지 배경에 흰색 테두리 박스 효과 주기
        pygame.draw.rect(screen, (40, 50, 70), (img_x - 10, img_y - 10, 280, 280), border_radius=15)
        pygame.draw.rect(screen, (100, 180, 220), (img_x - 10, img_y - 10, 280, 280), 3, border_radius=15)

        screen.blit(stage_image, (img_x, img_y))

        # 3. [게임 시작] 노란색 큰 버튼 렌더링
        btn_w, btn_h = 300, 70
        btn_x = w // 2 - btn_w // 2
        btn_y = h - 150

        # 버튼 외곽선 및 배경
        pygame.draw.rect(screen, (30, 90, 140), (btn_x, btn_y + 6, btn_w, btn_h), border_radius=12) # 그림자
        pygame.draw.rect(screen, (50, 140, 200), (btn_x, btn_y, btn_w, btn_h), border_radius=12) # 본체
        pygame.draw.rect(screen, (180, 230, 255), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=12) # 테두리

        btn_text = font_btn.render("게임 시작", True, (255, 255, 255))

        screen.blit(btn_text, (btn_x + btn_w // 2 - btn_text.get_width() // 2, btn_y + btn_h // 2 - btn_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # 엔터를 누르면 현재 스테이지 정보를 담아 게임으로 진입
                    game_data = {
                        "stage": current_stage_idx + 1,
                        "level": 1
                    }
                    pygame.quit()
                    return game_data

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 마우스 좌클릭
                    # [게임 시작] 버튼 클릭 판정
                    if btn_x <= event.pos[0] <= btn_x + btn_w and btn_y <= event.pos[1] <= btn_y + btn_h:
                        game_data = {
                            "stage": current_stage_idx + 1,
                            "level": 1
                        }
                        pygame.quit()
                        return game_data

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    run_menu()

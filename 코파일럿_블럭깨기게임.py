import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("코파일럿 블럭깨기 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLOCK_COLORS = [
    (255, 99, 71),      # Tomato
    (135, 206, 250),    # Light Sky Blue
    (255, 215, 0),      # Gold
    (144, 238, 144),    # Light Green
    (221, 160, 221),    # Plum
    (255, 20, 147),     # Deep Pink
    (0, 255, 255),      # Cyan
    (255, 140, 0),      # Dark Orange
    (0, 255, 127),      # Spring Green
    (186, 85, 211),     # Medium Orchid
]

# 폰트
FONT = pygame.font.SysFont("malgungothic", 36)

# 패들 클래스
class Paddle:
    def __init__(self):
        self.width = 360  # 기존 120에서 3배로 증가
        self.height = 20
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 40
        self.speed = 10

    def move(self, dx):
        self.x += dx * self.speed
        self.x = max(0, min(WIDTH - self.width, self.x))

    def draw(self):
        pygame.draw.rect(SCREEN, (30, 144, 255), (self.x, self.y, self.width, self.height), border_radius=10)

# 공 클래스
class Ball:
    def __init__(self):
        self.radius = 12
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-5, 5])
        self.dy = -5

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # 벽 충돌
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx *= -1
        if self.y <= self.radius:
            self.dy *= -1

    def draw(self):
        pygame.draw.circle(SCREEN, (255, 182, 193), (self.x, self.y), self.radius)

# 블럭 클래스
class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 80, 30)
        self.color = color
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(SCREEN, self.color, self.rect, border_radius=8)
            pygame.draw.rect(SCREEN, WHITE, self.rect, 2, border_radius=8)

# 블럭 생성
def create_blocks(rows=6, cols=7):
    blocks = []
    for row in range(rows):
        for col in range(cols):
            x = 20 + col * 85
            y = 60 + row * 35
            color = BLOCK_COLORS[(row * cols + col) % len(BLOCK_COLORS)]  # 더 다양한 색상 사용
            blocks.append(Block(x, y, color))
    return blocks

def main():
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()
    blocks = create_blocks()
    running = True
    score = 0

    while running:
        SCREEN.fill((25, 25, 40))

        # 게임 이름 표시
        title_text = FONT.render("블럭깨기", True, (255, 255, 0))
        SCREEN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 키 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-1)
        if keys[pygame.K_RIGHT]:
            paddle.move(1)

        ball.move()

        # 패들 충돌
        if pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height).collidepoint(ball.x, ball.y + ball.radius):
            ball.dy *= -1

        # 블럭 충돌
        for block in blocks:
            if block.alive and block.rect.collidepoint(ball.x, ball.y):
                block.alive = False
                ball.dy *= -1
                score += 10

        # 바닥에 닿으면 게임 오버
        if ball.y > HEIGHT:
            msg = FONT.render("게임 오버!", True, (255, 0, 0))
            SCREEN.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        # 모든 블럭 제거 시 클리어
        if all(not block.alive for block in blocks):
            msg = FONT.render("클리어!", True, (0, 255, 127))
            SCREEN.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        # 그리기
        paddle.draw()
        ball.draw()
        for block in blocks:
            block.draw()

        score_text = FONT.render(f"점수: {score}", True, WHITE)
        SCREEN.blit(score_text, (20, 50))  # 점수 위치 살짝 아래로 조정

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
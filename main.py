import pygame
import time

# Ініціалізація
pygame.init()

# Параметри вікна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

# Кольори
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 20, 100, 10)
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-6, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(6, 0)
    
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2, 20, 20)
        self.speed = [4, -4]
    
    def move(self):
        self.rect.move_ip(self.speed)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
    
    def check_collision(self, paddle, blocks):
        if self.rect.colliderect(paddle.rect):
            self.speed[1] = -self.speed[1]
        for block in blocks[:]:
            if self.rect.colliderect(block.rect):
                blocks.remove(block)
                self.speed[1] = -self.speed[1]
                break
        
    def draw(self):
        pygame.draw.ellipse(screen, BLUE, self.rect)

class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 20)
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = [Block(100 + i * 60, 50 + j * 30) for i in range(10) for j in range(4)]
        self.game_count = 0
        self.start_time = 0
        self.running = False
        self.font = pygame.font.Font(None, 30)






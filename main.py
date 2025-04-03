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
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

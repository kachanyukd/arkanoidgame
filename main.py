import pygame
import time
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
HISTORY_FILE = "game_history.json"

class Button:
    def __init__(self, text, x, y, width, height, border_radius=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 40)
        self.border_radius = border_radius
    
    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect, 0, border_radius=self.border_radius)
        pygame.draw.rect(screen, BLACK, self.rect, 5, border_radius=self.border_radius)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

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

    def reset(self):
        self.ball = Ball()
        self.blocks = [Block(100 + i * 60, 50 + j * 30) for i in range(10) for j in range(4)]
        self.start_time = time.time()
        self.game_count += 1

    def run(self):
        going = True
        while going:
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                if event.type == pygame.KEYDOWN and not self.running:
                    self.running = True
                    self.reset()
            
            if self.running:
                keys = pygame.key.get_pressed()
                self.paddle.move(keys)
                self.ball.move()
                self.ball.check_collision(self.paddle, self.blocks)
                if self.ball.rect.bottom >= HEIGHT or not self.blocks:
                    self.running = False
            
            for block in self.blocks:
                block.draw()
            self.paddle.draw()
            self.ball.draw()
            
            elapsed_time = int(time.time() - self.start_time) if self.running else 0
            info_text = f"Game: {self.game_count} | Time: {elapsed_time}s"
            text = self.font.render(info_text, True, (0, 0, 0))
            screen.blit(text, (10, 10))
            
            pygame.display.flip()
            pygame.time.delay(16)
        
        pygame.quit()

if __name__ == "__main__":
     game = Game()
     game.run()
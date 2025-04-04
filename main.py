import pygame
import time
import json

pygame.init()


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
MAROON = (128, 0, 0)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)  
DARK_BLUE = (0, 0, 139)
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
        pygame.draw.rect(screen, DARK_BLUE, self.rect)

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
        pygame.draw.ellipse(screen, DARK_GREEN, self.rect)

class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 20)
    
    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = [Block(100 + i * 60, 50 + j * 30) for i in range(10) for j in range(4)]
        self.game_count = 0
        self.start_time = 0
        self.running = False
        self.font = pygame.font.Font(None, 30)
        self.history = self.load_history()
        self.start_button = Button("START GAME", WIDTH // 2 - 150, HEIGHT // 2 - 120, 300, 80)
        self.history_button = Button("GAME HISTORY", WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 80)
        self.clear_history_button = Button("CLEAR HISTORY", WIDTH // 2 - 150, HEIGHT // 2 + 80, 300, 80)

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r") as file:
                data = json.load(file)
                if "games" not in data or "game_count" not in data:
                    data = {"games": [], "game_count": 1}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {"games": [], "game_count": 1}
    
    def save_history(self):
        with open(HISTORY_FILE, "w") as file:
            json.dump(self.history, file)

    def reset(self):
        self.ball = Ball()
        self.blocks = [Block(100 + i * 60, 50 + j * 30) for i in range(10) for j in range(4)]
        self.start_time = time.time()
        self.game_count += 1
        
    def show_history(self):
        screen.fill(WHITE)
        y_offset = 50
        title = self.font.render("Game History", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 60, 20))
        for i, record in enumerate(self.history["games"]):
            text = self.font.render(record, True, BLACK)
            screen.blit(text, (50, y_offset + i * 30))
        self.clear_history_button.draw()  
        pygame.display.flip()
        pygame.time.delay(2000)

    def clear_history(self):
        self.history["games"] = []  
        self.history["game_count"] = 0
        self.save_history()

    def run(self):
        while True:
            self.start_button.draw()
            self.history_button.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_history()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_clicked(event.pos):
                        self.running = True
                        self.reset()
                        self.game_loop()
                    elif self.history_button.is_clicked(event.pos):
                        self.show_history()
                    elif self.clear_history_button.is_clicked(event.pos):
                        self.clear_history()
            
    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_history()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return
            
            keys = pygame.key.get_pressed()
            self.paddle.move(keys)
            self.ball.move()
            self.ball.check_collision(self.paddle, self.blocks)
            
            if self.ball.rect.bottom >= HEIGHT or not self.blocks:
                elapsed_time = int(time.time() - self.start_time)
                self.history["games"].append(f"Game {self.history['game_count']}: {elapsed_time}s")
                self.save_history()
                self.running = False
                return
            
            for block in self.blocks:
                block.draw()
            self.paddle.draw()
            self.ball.draw()
            
            elapsed_time = int(time.time() - self.start_time)
            info_text = f"Game: {self.history['game_count']} | Time: {elapsed_time}s"
            text = self.font.render(info_text, True, BLACK)

            screen.blit(text, (10, 10))
            
            pygame.display.flip()
            pygame.time.delay(16)

if __name__ == "__main__":
    game = Game()
    game.run()
import pytest
from main import Paddle, Ball, Block, Game

# Paddle movement test
def test_paddle_movement_right():
    paddle = Paddle()
    start_x = paddle.rect.x

    class Keys:
        def __getitem__(self, key):
            return key == 1073741903  # pygame.K_RIGHT

    paddle.move(Keys())
    assert paddle.rect.x > start_x, "Paddle should move right"

def test_paddle_movement_left():
    paddle = Paddle()
    paddle.rect.x = 100
    start_x = paddle.rect.x

    class Keys:
        def __getitem__(self, key):
            return key == 1073741904  # pygame.K_LEFT

    paddle.move(Keys())
    assert paddle.rect.x < start_x, "Paddle should move left"

# Ball bounce tests
def test_ball_bounce_left_wall():
    ball = Ball()
    ball.rect.left = 0
    ball.speed = [-4, -4]
    ball.move()
    assert ball.speed[0] == 4, "Ball should bounce from left wall"

def test_ball_bounce_right_wall():
    ball = Ball()
    ball.rect.right = 800  # WIDTH
    ball.speed = [4, -4]
    ball.move()
    assert ball.speed[0] == -4, "Ball should bounce from right wall"

def test_ball_bounce_top_wall():
    ball = Ball()
    ball.rect.top = 0
    ball.speed = [4, -4]
    ball.move()
    assert ball.speed[1] == 4, "Ball should bounce from top wall"

# Ball and block collision
def test_ball_block_collision_removes_block():
    ball = Ball()
    block = Block(100, 100)
    block.rect.topleft = ball.rect.topleft
    blocks = [block]
    paddle = Paddle()

    ball.check_collision(paddle, blocks)
    assert block not in blocks, "Block should be removed on collision"

# Game history
def test_game_history_add():
    game = Game()
    initial_count = len(game.history["games"])
    game.history["games"].append("Game test: 5s")
    game.save_history()

    # Reload history
    game.history = game.load_history()
    assert len(game.history["games"]) >= initial_count + 1, "Game history should be saved and loaded"

def test_clear_history():
    game = Game()
    game.history["games"] = ["Game 1: 10s", "Game 2: 15s"]
    game.history["game_count"] = 5
    game.clear_history()

    assert game.history["games"] == [], "Game history should be cleared"
    assert game.history["game_count"] == 0, "Game count should be reset"
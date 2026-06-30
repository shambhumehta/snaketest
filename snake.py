import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 650, 650
CELL_SIZE = 30
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 180, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 24)
big_font = pygame.font.SysFont("monospace", 48)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def place_food(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos

def reset_game():
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    food = place_food(snake)
    score = 0
    return snake, direction, food, score

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        title = big_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Score: {score}", True, WHITE)
        restart_text = font.render("Press SPACE to play again", True, WHITE)
        quit_text = font.render("Press ESC to quit", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

snake, direction, food, score = reset_game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if head == food:
        snake.insert(0, head)
        score += 1
        food = place_food(snake)
    else:
        snake.insert(0, head)
        snake.pop()

    if (head[0] < 0 or head[0] >= COLS or
        head[1] < 0 or head[1] >= ROWS or
        head in snake[1:]):
        game_over_screen(score)
        snake, direction, food, score = reset_game()
        continue

    screen.fill(BLACK)
    draw_grid()

    for i, segment in enumerate(snake):
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(screen, color,
                         (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK,
                         (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE), 1)

    pygame.draw.rect(screen, RED,
                     (food[0] * CELL_SIZE, food[1] * CELL_SIZE,
                      CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLACK,
                     (food[0] * CELL_SIZE, food[1] * CELL_SIZE,
                      CELL_SIZE, CELL_SIZE), 1)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()

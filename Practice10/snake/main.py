import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL = 20

# Grid size
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

# Clock
clock = pygame.time.Clock()

# Initial snake settings
snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)

# Initial score and level
score = 0
level = 1

# Initial speed
speed = 8

# Walls list
walls = []

# Number of foods needed to go to next level
FOODS_TO_NEXT_LEVEL = 4


def generate_walls(current_level):
    """
    Generate wall positions depending on level.
    Level 1: no inner walls
    Level 2: horizontal wall in the middle
    Level 3+: horizontal + vertical walls
    """
    wall_positions = []

    if current_level >= 2:
        # Horizontal wall in the middle
        for x in range(10, 20):
            wall_positions.append((x, 12))

    if current_level >= 3:
        # Vertical wall in the middle
        for y in range(15, 25):
            wall_positions.append((15, y))

    return wall_positions


def random_food_position():
    """
    Generate random food position so that food
    does not appear on snake or on walls.
    """
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

        if pos not in snake and pos not in walls:
            return pos


# First food generation
food = random_food_position()


def draw_cell(position, color):
    """
    Draw one square cell at given grid position.
    """
    x, y = position
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))


def draw_snake():
    """
    Draw snake body.
    Head is darker than the body.
    """
    for i, part in enumerate(snake):
        if i == 0:
            draw_cell(part, DARK_GREEN)
        else:
            draw_cell(part, GREEN)


def draw_walls():
    """
    Draw wall blocks.
    """
    for wall in walls:
        draw_cell(wall, GRAY)


def move_snake():
    """
    Move snake by adding a new head in current direction.
    If food is not eaten, remove the tail.
    """
    global snake, food, score, level, speed, walls

    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Check border collision
    if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
        game_over()

    # Check collision with itself
    if new_head in snake:
        game_over()

    # Check collision with wall
    if new_head in walls:
        game_over()

    # Add new head
    snake.insert(0, new_head)

    # If snake eats food
    if new_head == food:
        score += 1
        food = random_food_position()

        # Level up after every 4 foods
        if score % FOODS_TO_NEXT_LEVEL == 0:
            level += 1
            speed += 2
            walls = generate_walls(level)

            # Regenerate food so it does not appear inside new walls
            while food in walls or food in snake:
                food = random_food_position()
    else:
        # Remove tail if food not eaten
        snake.pop()


def game_over():
    """
    Show game over text and exit game.
    """
    screen.fill(WHITE)
    text = big_font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)

    screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
    screen.blit(level_text, (WIDTH // 2 - 45, HEIGHT // 2 + 40))

    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


# Main game loop
running = True
walls = generate_walls(level)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Move snake
    move_snake()

    # Draw everything
    screen.fill(WHITE)
    draw_walls()
    draw_snake()
    draw_cell(food, RED)

    # Draw score and level counters
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
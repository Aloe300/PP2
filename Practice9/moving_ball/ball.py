import pygame


WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
RED = (220, 30, 30)
BLACK = (25, 25, 25)


class Ball:
    def __init__(self, x, y, radius, step):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step

    def move(self, dx, dy, screen_width, screen_height):
        new_x = self.x + dx
        new_y = self.y + dy

        if self.radius <= new_x <= screen_width - self.radius:
            self.x = new_x

        if self.radius <= new_y <= screen_height - self.radius:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)


class MovingBallApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Moving Ball")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 28)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, 25, 20)

    def draw(self):
        self.screen.fill(WHITE)
        self.ball.draw(self.screen)
        text = self.font.render("Use arrow keys to move the ball", True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.ball.move(-self.ball.step, 0, WIDTH, HEIGHT)
                    elif event.key == pygame.K_RIGHT:
                        self.ball.move(self.ball.step, 0, WIDTH, HEIGHT)
                    elif event.key == pygame.K_UP:
                        self.ball.move(0, -self.ball.step, WIDTH, HEIGHT)
                    elif event.key == pygame.K_DOWN:
                        self.ball.move(0, self.ball.step, WIDTH, HEIGHT)

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

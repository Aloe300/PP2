import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (70, 70, 70)
BLUE = (60, 130, 240)
GREEN = (40, 180, 90)
RED = (220, 50, 50)
YELLOW = (230, 200, 30)


class Button:
    def __init__(self, x, y, w, h, text, font, color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        draw_color = self.color
        if self.rect.collidepoint(mouse_pos):
            draw_color = tuple(min(255, c + 25) for c in self.color)
        pygame.draw.rect(surface, draw_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(surface, text, font, color, y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(rendered, rect)


def ask_username(screen, clock):
    font_big = pygame.font.SysFont("Verdana", 36)
    font_small = pygame.font.SysFont("Verdana", 22)
    name = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12 and event.unicode.isprintable():
                        name += event.unicode

        screen.fill((35, 35, 35))
        draw_center_text(screen, "Enter username", font_big, WHITE, 170)
        pygame.draw.rect(screen, WHITE, (80, 250, 240, 50), border_radius=8)
        text_surface = font_small.render(name, True, BLACK)
        screen.blit(text_surface, (95, 260))
        draw_center_text(screen, "Press Enter to start", font_small, WHITE, 350)
        pygame.display.update()
        clock.tick(60)

from collections import deque
import math
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def make_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def draw_pencil_line(surface, start, end, color, width):
    pygame.draw.line(surface, color, start, end, width)
    pygame.draw.circle(surface, color, start, width // 2)
    pygame.draw.circle(surface, color, end, width // 2)


def draw_shape(surface, tool, start, end, color, width):
    if tool == "rectangle":
        pygame.draw.rect(surface, color, make_rect(start, end), width)

    elif tool == "circle":
        radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        pygame.draw.circle(surface, color, start, radius, width)

    elif tool == "line":
        pygame.draw.line(surface, color, start, end, width)

    elif tool == "square":
        x1, y1 = start
        x2, y2 = end
        side = min(abs(x2 - x1), abs(y2 - y1))
        x2 = x1 + side if x2 >= x1 else x1 - side
        y2 = y1 + side if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, color, make_rect(start, (x2, y2)), width)

    elif tool == "right_triangle":
        x1, y1 = start
        x2, y2 = end
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "equilateral_triangle":
        x1, y1 = start
        x2, y2 = end
        base = x2 - x1
        height = abs(base) * math.sqrt(3) / 2
        direction = -1 if y2 < y1 else 1
        points = [
            (x1, y1),
            (x2, y1),
            ((x1 + x2) // 2, int(y1 + direction * height)),
        ]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "rhombus":
        x1, y1 = start
        x2, y2 = end
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        points = [
            (center_x, y1),
            (x2, center_y),
            (center_x, y2),
            (x1, center_y),
        ]
        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(fill_color)

    if target_color == fill_color:
        return

    queue = deque([(x, y)])
    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))

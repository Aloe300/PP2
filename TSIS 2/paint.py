import os
from datetime import datetime
import pygame

from tools import draw_pencil_line, draw_shape, flood_fill, WHITE, BLACK


WIDTH, HEIGHT = 900, 650
TOOLBAR_HEIGHT = 90
CANVAS_WIDTH = WIDTH
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

SMALL = 2
MEDIUM = 5
LARGE = 10

COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 180, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 220, 0),
    "purple": (150, 0, 180),
}


def canvas_pos(mouse_pos):
    return mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT


def is_on_canvas(mouse_pos):
    return mouse_pos[1] >= TOOLBAR_HEIGHT


def save_canvas(canvas):
    os.makedirs("saves", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("saves", f"paint_{timestamp}.png")
    pygame.image.save(canvas, filename)
    return filename


def draw_toolbar(screen, font, tool, color, brush_size, saved_message, text_mode):
    pygame.draw.rect(screen, (35, 35, 35), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    line1 = (
        "Tools: P Pencil | L Line | R Rect | O Circle | S Square | "
        "T RightTriangle | Y Equilateral | H Rhombus | F Fill | X Text | E Eraser"
    )
    line2 = (
        "Brush: 1 Small 2 Medium 3 Large | Colors: B Blue G Green K Black A Red V Purple Z Yellow | "
        "Ctrl+S Save | Backspace Clear | Esc Cancel/Exit"
    )
    status = f"Current tool: {tool} | size: {brush_size}px | color: {color}"
    if text_mode:
        status += " | TEXT MODE: type, Enter confirm, Esc cancel"
    if saved_message:
        status += f" | Saved: {saved_message}"

    screen.blit(font.render(line1, True, WHITE), (10, 8))
    screen.blit(font.render(line2, True, WHITE), (10, 32))
    screen.blit(font.render(status, True, WHITE), (10, 58))

    pygame.draw.rect(screen, color, (WIDTH - 55, 20, 35, 35))
    pygame.draw.rect(screen, WHITE, (WIDTH - 55, 20, 35, 35), 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Extended Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    text_font = pygame.font.SysFont("Arial", 28)

    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)

    tool = "pencil"
    color = COLORS["blue"]
    brush_size = MEDIUM

    drawing = False
    start_pos = None
    current_pos = None
    last_pos = None

    text_mode = False
    text_pos = None
    text_value = ""

    saved_message = ""

    running = True
    while running:
        ctrl_held = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]
        alt_held = pygame.key.get_pressed()[pygame.K_LALT] or pygame.key.get_pressed()[pygame.K_RALT]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and alt_held:
                    running = False

                elif event.key == pygame.K_s and ctrl_held:
                    saved_message = save_canvas(canvas)

                elif text_mode:
                    if event.key == pygame.K_RETURN:
                        rendered_text = text_font.render(text_value, True, color)
                        canvas.blit(rendered_text, text_pos)
                        text_mode = False
                        text_pos = None
                        text_value = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        text_pos = None
                        text_value = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]
                    else:
                        text_value += event.unicode

                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_BACKSPACE:
                        canvas.fill(WHITE)

                    elif event.key == pygame.K_1:
                        brush_size = SMALL
                    elif event.key == pygame.K_2:
                        brush_size = MEDIUM
                    elif event.key == pygame.K_3:
                        brush_size = LARGE

                    elif event.key == pygame.K_p:
                        tool = "pencil"
                    elif event.key == pygame.K_l:
                        tool = "line"
                    elif event.key == pygame.K_r:
                        tool = "rectangle"
                    elif event.key == pygame.K_o:
                        tool = "circle"
                    elif event.key == pygame.K_s:
                        tool = "square"
                    elif event.key == pygame.K_t:
                        tool = "right_triangle"
                    elif event.key == pygame.K_y:
                        tool = "equilateral_triangle"
                    elif event.key == pygame.K_h:
                        tool = "rhombus"
                    elif event.key == pygame.K_f:
                        tool = "fill"
                    elif event.key == pygame.K_x:
                        tool = "text"
                    elif event.key == pygame.K_e:
                        tool = "eraser"

                    elif event.key == pygame.K_b:
                        color = COLORS["blue"]
                    elif event.key == pygame.K_g:
                        color = COLORS["green"]
                    elif event.key == pygame.K_k:
                        color = COLORS["black"]
                    elif event.key == pygame.K_a:
                        color = COLORS["red"]
                    elif event.key == pygame.K_v:
                        color = COLORS["purple"]
                    elif event.key == pygame.K_z:
                        color = COLORS["yellow"]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and is_on_canvas(event.pos):
                    pos = canvas_pos(event.pos)
                    saved_message = ""

                    if tool == "pencil":
                        drawing = True
                        last_pos = pos
                        pygame.draw.circle(canvas, color, pos, brush_size // 2)

                    elif tool == "eraser":
                        drawing = True
                        last_pos = pos
                        pygame.draw.circle(canvas, WHITE, pos, brush_size)

                    elif tool == "fill":
                        flood_fill(canvas, pos, color)

                    elif tool == "text":
                        text_mode = True
                        text_pos = pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = pos
                        current_pos = pos

            elif event.type == pygame.MOUSEMOTION:
                if drawing and is_on_canvas(event.pos):
                    pos = canvas_pos(event.pos)
                    current_pos = pos

                    if tool == "pencil" and last_pos is not None:
                        draw_pencil_line(canvas, last_pos, pos, color, brush_size)
                        last_pos = pos

                    elif tool == "eraser" and last_pos is not None:
                        draw_pencil_line(canvas, last_pos, pos, WHITE, brush_size * 2)
                        last_pos = pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing and is_on_canvas(event.pos):
                    end_pos = canvas_pos(event.pos)

                    if tool not in ("pencil", "eraser"):
                        draw_shape(canvas, tool, start_pos, end_pos, color, brush_size)

                    drawing = False
                    start_pos = None
                    current_pos = None
                    last_pos = None

        screen.fill((70, 70, 70))
        draw_toolbar(screen, font, tool, color, brush_size, saved_message, text_mode)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        if drawing and start_pos and current_pos and tool not in ("pencil", "eraser"):
            preview = canvas.copy()
            draw_shape(preview, tool, start_pos, current_pos, color, brush_size)
            screen.blit(preview, (0, TOOLBAR_HEIGHT))

        if text_mode and text_pos is not None:
            preview_text = text_font.render(text_value + "|", True, color)
            screen.blit(preview_text, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

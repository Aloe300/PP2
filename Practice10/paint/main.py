import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    radius = 15
    color = (0, 0, 255)   # default blue
    tool = 'brush'        # brush, rectangle, circle, eraser

    points = []           # points for free drawing
    drawing = False       # for rectangle/circle
    start_pos = None
    current_pos = None

    shapes = []           # store rectangles and circles

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # color selection
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_k:
                    color = (0, 0, 0)

                # tool selection
                elif event.key == pygame.K_1:
                    tool = 'brush'
                elif event.key == pygame.K_2:
                    tool = 'rectangle'
                elif event.key == pygame.K_3:
                    tool = 'circle'
                elif event.key == pygame.K_e:
                    tool = 'eraser'
                elif event.key == pygame.K_c:
                    points.clear()
                    shapes.clear()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if tool == 'brush' or tool == 'eraser':
                        points.append((event.pos, color if tool == 'brush' else (0, 0, 0), radius if tool == 'brush' else 20))
                    else:
                        drawing = True
                        start_pos = event.pos
                        current_pos = event.pos

                elif event.button == 3:
                    radius = max(1, radius - 1)

                elif event.button == 4:
                    radius = min(200, radius + 1)

            if event.type == pygame.MOUSEMOTION:
                if tool == 'brush' and pygame.mouse.get_pressed()[0]:
                    points.append((event.pos, color, radius))
                    points[:] = points[-256:]

                elif tool == 'eraser' and pygame.mouse.get_pressed()[0]:
                    points.append((event.pos, (0, 0, 0), 20))
                    points[:] = points[-256:]

                elif drawing:
                    current_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    if tool == 'rectangle':
                        rect = make_rect(start_pos, event.pos)
                        shapes.append(('rectangle', rect, color))
                    elif tool == 'circle':
                        center = start_pos
                        radius_circle = int(((event.pos[0] - start_pos[0]) ** 2 + (event.pos[1] - start_pos[1]) ** 2) ** 0.5)
                        shapes.append(('circle', center, radius_circle, color))

                    drawing = False
                    start_pos = None
                    current_pos = None

        screen.fill((0, 0, 0))

        # draw free brush/eraser points
        for i in range(len(points) - 1):
            start, start_color, start_radius = points[i]
            end, _, _ = points[i + 1]
            drawLineBetween(screen, start, end, start_radius, start_color)

        # draw saved shapes
        for shape in shapes:
            if shape[0] == 'rectangle':
                _, rect, shape_color = shape
                pygame.draw.rect(screen, shape_color, rect, 2)
            elif shape[0] == 'circle':
                _, center, radius_circle, shape_color = shape
                pygame.draw.circle(screen, shape_color, center, radius_circle, 2)

        # preview while dragging rectangle/circle
        if drawing and start_pos and current_pos:
            if tool == 'rectangle':
                rect = make_rect(start_pos, current_pos)
                pygame.draw.rect(screen, color, rect, 2)
            elif tool == 'circle':
                radius_circle = int(((current_pos[0] - start_pos[0]) ** 2 + (current_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

        # info text
        info = f"Tool: {tool} | 1-Brush 2-Rectangle 3-Circle E-Eraser | R/G/B/K color | Mouse wheel/right click size down/up | C-clear"
        text = font.render(info, True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


def make_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return pygame.Rect(left, top, width, height)


main()
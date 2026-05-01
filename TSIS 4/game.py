import pygame
import random
import json
import os
import sys

import db


WIDTH = 600
HEIGHT = 600
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (210, 210, 210)
DARK_GRAY = (60, 60, 60)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 140, 0)
RED = (240, 30, 30)
DARK_RED = (130, 0, 0)
BLUE = (40, 120, 255)
PURPLE = (150, 70, 220)
YELLOW = (245, 190, 0)
ORANGE = (245, 130, 30)
CYAN = (0, 190, 210)

SETTINGS_FILE = "settings.json"
FOODS_TO_NEXT_LEVEL = 4
POWERUP_FIELD_TIMEOUT = 8000
POWERUP_EFFECT_DURATION = 5000


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font, mouse_pos):
        color = (180, 180, 180) if self.rect.collidepoint(mouse_pos) else (220, 220, 220)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        text = font.render(self.text, True, BLACK)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class SnakeApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Extended")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.big_font = pygame.font.SysFont("Arial", 48)

        self.settings = self.load_settings()
        self.username = ""
        self.db_ready = False

        try:
            db.setup_database()
            self.db_ready = True
        except Exception as e:
            print("Database setup error:", e)

        self.state = "menu"
        self.last_result = None

    def load_settings(self):
        default_settings = {
            "snake_color": [0, 200, 0],
            "grid_overlay": True,
            "sound": True,
        }

        if not os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "w") as file:
                json.dump(default_settings, file, indent=4)
            return default_settings

        try:
            with open(SETTINGS_FILE, "r") as file:
                data = json.load(file)

            for key in default_settings:
                if key not in data:
                    data[key] = default_settings[key]

            return data
        except Exception:
            return default_settings

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def run(self):
        while True:
            if self.state == "menu":
                self.main_menu()
            elif self.state == "play":
                self.play_game()
            elif self.state == "leaderboard":
                self.leaderboard_screen()
            elif self.state == "settings":
                self.settings_screen()
            elif self.state == "game_over":
                self.game_over_screen()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def draw_center_text(self, text, font, color, y):
        rendered = font.render(text, True, color)
        self.screen.blit(rendered, rendered.get_rect(center=(WIDTH // 2, y)))

    def main_menu(self):
        buttons = [
            Button(210, 250, 180, 45, "Play"),
            Button(210, 310, 180, 45, "Leaderboard"),
            Button(210, 370, 180, 45, "Settings"),
            Button(210, 430, 180, 45, "Quit"),
        ]

        entering_name = True

        while self.state == "menu":
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN and entering_name:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        entering_name = False
                    else:
                        if len(self.username) < 16 and event.unicode.isprintable():
                            self.username += event.unicode

                if buttons[0].clicked(event):
                    if self.username.strip() == "":
                        self.username = "Player"
                    self.state = "play"
                elif buttons[1].clicked(event):
                    self.state = "leaderboard"
                elif buttons[2].clicked(event):
                    self.state = "settings"
                elif buttons[3].clicked(event):
                    self.quit_game()

            self.screen.fill(WHITE)
            self.draw_center_text("SNAKE", self.big_font, DARK_GREEN, 90)
            self.draw_center_text("Enter username:", self.font, BLACK, 150)

            name_box = pygame.Rect(170, 175, 260, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), name_box)
            pygame.draw.rect(self.screen, BLACK, name_box, 2)
            name_text = self.font.render(self.username + ("|" if entering_name else ""), True, BLACK)
            self.screen.blit(name_text, (name_box.x + 10, name_box.y + 8))

            if not self.db_ready:
                warning = self.small_font.render("DB not connected. Check database.ini", True, RED)
                self.screen.blit(warning, (150, 220))

            for button in buttons:
                button.draw(self.screen, self.font, mouse)

            pygame.display.flip()
            self.clock.tick(60)

    def settings_screen(self):
        color_options = [
            ("Green", [0, 200, 0]),
            ("Blue", [40, 120, 255]),
            ("Purple", [150, 70, 220]),
            ("Orange", [245, 130, 30]),
        ]

        back = Button(200, 500, 200, 45, "Save & Back")

        while self.state == "settings":
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                    elif event.key == pygame.K_s:
                        self.settings["sound"] = not self.settings["sound"]
                    elif event.key == pygame.K_1:
                        self.settings["snake_color"] = color_options[0][1]
                    elif event.key == pygame.K_2:
                        self.settings["snake_color"] = color_options[1][1]
                    elif event.key == pygame.K_3:
                        self.settings["snake_color"] = color_options[2][1]
                    elif event.key == pygame.K_4:
                        self.settings["snake_color"] = color_options[3][1]
                    elif event.key == pygame.K_ESCAPE:
                        self.save_settings()
                        self.state = "menu"

                if back.clicked(event):
                    self.save_settings()
                    self.state = "menu"

            self.screen.fill(WHITE)
            self.draw_center_text("SETTINGS", self.big_font, BLACK, 80)

            grid_line = f"G - Grid overlay: {'ON' if self.settings['grid_overlay'] else 'OFF'}"
            sound_line = f"S - Sound: {'ON' if self.settings['sound'] else 'OFF'}"

            self.screen.blit(self.font.render(grid_line, True, BLACK), (120, 160))
            self.screen.blit(self.font.render(sound_line, True, BLACK), (120, 205))

            self.screen.blit(self.font.render("Snake color:", True, BLACK), (120, 260))
            y = 300
            for index, (name, rgb) in enumerate(color_options, start=1):
                pygame.draw.rect(self.screen, rgb, (130, y, 30, 30))
                label = f"{index} - {name}"
                if self.settings["snake_color"] == rgb:
                    label += "  selected"
                self.screen.blit(self.font.render(label, True, BLACK), (175, y + 3))
                y += 45

            back.draw(self.screen, self.font, mouse)
            pygame.display.flip()
            self.clock.tick(60)

    def leaderboard_screen(self):
        back = Button(220, 530, 160, 40, "Back")

        while self.state == "leaderboard":
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                if back.clicked(event):
                    self.state = "menu"

            self.screen.fill(WHITE)
            self.draw_center_text("LEADERBOARD", self.big_font, BLACK, 60)

            if self.db_ready:
                rows = db.get_top_scores(10)
            else:
                rows = []

            header = self.small_font.render("Rank   Name              Score   Level   Date", True, BLACK)
            self.screen.blit(header, (45, 120))

            y = 160
            if not rows:
                self.draw_center_text("No scores yet or database is not connected.", self.font, RED, 260)
            else:
                for i, row in enumerate(rows, start=1):
                    username, score, level, date = row
                    line = f"{i:<5} {username[:14]:<16} {score:<7} {level:<6} {date}"
                    self.screen.blit(self.small_font.render(line, True, BLACK), (45, y))
                    y += 32

            back.draw(self.screen, self.font, mouse)
            pygame.display.flip()
            self.clock.tick(60)

    def game_over_screen(self):
        retry = Button(190, 370, 220, 45, "Retry")
        menu = Button(190, 430, 220, 45, "Main Menu")

        while self.state == "game_over":
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if retry.clicked(event):
                    self.state = "play"
                elif menu.clicked(event):
                    self.state = "menu"

            self.screen.fill(WHITE)
            self.draw_center_text("GAME OVER", self.big_font, RED, 130)

            if self.last_result:
                score = self.last_result["score"]
                level = self.last_result["level"]
                best = self.last_result["personal_best"]
                self.draw_center_text(f"Final Score: {score}", self.font, BLACK, 220)
                self.draw_center_text(f"Level Reached: {level}", self.font, BLACK, 255)
                self.draw_center_text(f"Personal Best: {best}", self.font, BLACK, 290)

            retry.draw(self.screen, self.font, mouse)
            menu.draw(self.screen, self.font, mouse)

            pygame.display.flip()
            self.clock.tick(60)

    def random_empty_cell(self, snake, walls, occupied=None):
        if occupied is None:
            occupied = []

        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in snake and pos not in walls and pos not in occupied:
                return pos

    def make_food(self, snake, walls, occupied):
        choices = [
            {"kind": "normal", "points": 1, "color": RED, "lifetime": None},
            {"kind": "bonus", "points": 3, "color": YELLOW, "lifetime": 5000},
            {"kind": "big", "points": 5, "color": ORANGE, "lifetime": 4000},
        ]
        food = random.choice(choices).copy()
        food["pos"] = self.random_empty_cell(snake, walls, occupied)
        food["created_at"] = pygame.time.get_ticks()
        return food

    def make_poison(self, snake, walls, occupied):
        return {
            "pos": self.random_empty_cell(snake, walls, occupied),
            "created_at": pygame.time.get_ticks(),
        }

    def make_powerup(self, snake, walls, occupied):
        kind = random.choice(["speed", "slow", "shield"])
        colors = {
            "speed": CYAN,
            "slow": PURPLE,
            "shield": BLUE,
        }
        return {
            "kind": kind,
            "pos": self.random_empty_cell(snake, walls, occupied),
            "created_at": pygame.time.get_ticks(),
            "color": colors[kind],
        }

    def generate_obstacles(self, level, snake):
        if level < 3:
            return []

        count = min(5 + level * 2, 28)
        walls = []
        head = snake[0]

        safe_area = set()
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                safe_area.add((head[0] + dx, head[1] + dy))

        tries = 0
        while len(walls) < count and tries < 500:
            tries += 1
            pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))

            if pos in snake or pos in walls or pos in safe_area:
                continue

            # Keep the four immediate directions around the head free.
            near_head = [
                (head[0] + 1, head[1]),
                (head[0] - 1, head[1]),
                (head[0], head[1] + 1),
                (head[0], head[1] - 1),
            ]
            if pos in near_head:
                continue

            walls.append(pos)

        return walls

    def draw_cell(self, pos, color):
        x, y = pos
        rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 1)

    def draw_grid(self):
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, LIGHT_GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, LIGHT_GRAY, (0, y), (WIDTH, y))

    def play_game(self):
        snake = [(5, 5), (4, 5), (3, 5)]
        direction = (1, 0)
        next_direction = direction

        score = 0
        level = 1
        foods_eaten_this_level = 0
        base_speed = 8

        walls = self.generate_obstacles(level, snake)

        food = self.make_food(snake, walls, [])
        poison = self.make_poison(snake, walls, [food["pos"]])
        powerup = None
        last_powerup_spawn = pygame.time.get_ticks()

        active_powerup = None
        active_until = 0
        shield_ready = False

        if self.db_ready:
            personal_best = db.get_personal_best(self.username or "Player")
        else:
            personal_best = 0

        # Use ticks instead of resetting pygame timers every frame.
        # Resetting set_timer constantly can prevent the move event from firing.
        last_move_time = pygame.time.get_ticks()

        game_running = True

        while game_running and self.state == "play":
            now = pygame.time.get_ticks()

            current_speed = base_speed
            if active_powerup == "speed" and now < active_until:
                current_speed = base_speed + 5
            elif active_powerup == "slow" and now < active_until:
                current_speed = max(3, base_speed - 4)
            elif active_powerup in ["speed", "slow"] and now >= active_until:
                active_powerup = None
                active_until = 0

            move_delay = max(50, 1000 // current_speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        next_direction = (1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        return

            if now - last_move_time >= move_delay:
                last_move_time = now
                direction = next_direction
                head_x, head_y = snake[0]
                dx, dy = direction
                new_head = (head_x + dx, head_y + dy)

                collision = (
                    new_head[0] < 0 or new_head[0] >= COLS or
                    new_head[1] < 0 or new_head[1] >= ROWS or
                    new_head in snake or
                    new_head in walls
                )

                if collision:
                    if shield_ready:
                        shield_ready = False
                        active_powerup = None

                        # Keep snake inside if wall collision happens.
                        safe_x = min(max(new_head[0], 0), COLS - 1)
                        safe_y = min(max(new_head[1], 0), ROWS - 1)
                        new_head = (safe_x, safe_y)

                        if new_head in snake or new_head in walls:
                            new_head = snake[0]
                    else:
                        game_running = False
                        break

                snake.insert(0, new_head)

                grew = False

                if new_head == food["pos"]:
                    score += food["points"]
                    grew = True
                    foods_eaten_this_level += 1
                    occupied = [poison["pos"]] if poison else []
                    if powerup:
                        occupied.append(powerup["pos"])
                    food = self.make_food(snake, walls, occupied)

                    if foods_eaten_this_level >= FOODS_TO_NEXT_LEVEL:
                        foods_eaten_this_level = 0
                        level += 1
                        base_speed += 2
                        walls = self.generate_obstacles(level, snake)
                        occupied = [food["pos"]]
                        if poison:
                            occupied.append(poison["pos"])
                        if powerup:
                            occupied.append(powerup["pos"])
                        if food["pos"] in walls:
                            food = self.make_food(snake, walls, occupied)

                if poison and new_head == poison["pos"]:
                    for _ in range(2):
                        if len(snake) > 0:
                            snake.pop()
                    if len(snake) <= 1:
                        game_running = False
                        break
                    poison = self.make_poison(snake, walls, [food["pos"]])
                    grew = True

                if powerup and new_head == powerup["pos"]:
                    active_powerup = powerup["kind"]

                    if active_powerup == "shield":
                        shield_ready = True
                        active_until = 0
                    else:
                        shield_ready = False
                        active_until = now + POWERUP_EFFECT_DURATION

                    powerup = None
                    last_powerup_spawn = now
                    grew = True

                if not grew:
                    snake.pop()


            # Food timeout from Practice 11 behavior.
            if food["lifetime"] and now - food["created_at"] > food["lifetime"]:
                occupied = [poison["pos"]] if poison else []
                if powerup:
                    occupied.append(powerup["pos"])
                food = self.make_food(snake, walls, occupied)

            # Poison respawn timer.
            if poison and now - poison["created_at"] > 9000:
                poison = self.make_poison(snake, walls, [food["pos"]])

            # Only one power-up on field at a time.
            if powerup is None and active_powerup is None and now - last_powerup_spawn > 7000:
                occupied = [food["pos"]]
                if poison:
                    occupied.append(poison["pos"])
                powerup = self.make_powerup(snake, walls, occupied)

            if powerup and now - powerup["created_at"] > POWERUP_FIELD_TIMEOUT:
                powerup = None
                last_powerup_spawn = now

            self.screen.fill(WHITE)

            if self.settings["grid_overlay"]:
                self.draw_grid()

            for wall in walls:
                self.draw_cell(wall, GRAY)

            self.draw_cell(food["pos"], food["color"])

            if poison:
                self.draw_cell(poison["pos"], DARK_RED)

            if powerup:
                self.draw_cell(powerup["pos"], powerup["color"])

            snake_color = tuple(self.settings["snake_color"])
            for i, part in enumerate(snake):
                if i == 0:
                    self.draw_cell(part, DARK_GREEN)
                else:
                    self.draw_cell(part, snake_color)

            info = [
                f"Player: {self.username or 'Player'}",
                f"Score: {score}",
                f"Level: {level}",
                f"Best: {personal_best}",
            ]

            x = 10
            y = 8
            for item in info:
                text = self.small_font.render(item, True, BLACK)
                self.screen.blit(text, (x, y))
                y += 22

            if active_powerup == "speed" and now < active_until:
                remaining = max(0, (active_until - now) // 1000 + 1)
                text = self.small_font.render(f"Power-up: SPEED {remaining}s", True, BLUE)
                self.screen.blit(text, (360, 8))
            elif active_powerup == "slow" and now < active_until:
                remaining = max(0, (active_until - now) // 1000 + 1)
                text = self.small_font.render(f"Power-up: SLOW {remaining}s", True, PURPLE)
                self.screen.blit(text, (360, 8))
            elif shield_ready:
                text = self.small_font.render("Power-up: SHIELD", True, BLUE)
                self.screen.blit(text, (360, 8))
            else:
                text = self.small_font.render("Power-up: none", True, DARK_GRAY)
                self.screen.blit(text, (360, 8))

            pygame.display.flip()
            self.clock.tick(60)

        # Save result after game over.
        if self.db_ready:
            try:
                db.save_result(self.username or "Player", score, level)
                personal_best = max(personal_best, score)
            except Exception as e:
                print("Could not save result:", e)

        self.last_result = {
            "score": score,
            "level": level,
            "personal_best": personal_best,
        }

        self.state = "game_over"

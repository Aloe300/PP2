import os
import random
import pygame
from pygame.locals import *
from persistence import save_score

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ROAD_LEFT = 40
ROAD_RIGHT = 360
LANES = [80, 160, 240, 320]
FINISH_DISTANCE = 3000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (40, 200, 90)
BLUE = (60, 160, 255)
YELLOW = (255, 220, 40)
ORANGE = (255, 140, 40)
PURPLE = (170, 80, 220)
GRAY = (120, 120, 120)
DARK_GRAY = (55, 55, 55)
BROWN = (120, 70, 30)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


def load_image(name, size=None):
    image = pygame.image.load(os.path.join(ASSET_DIR, name)).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image


def recolor_car(image, color_name):
    color_map = {
        "blue": BLUE,
        "red": RED,
        "green": GREEN,
        "yellow": YELLOW,
    }
    overlay_color = color_map.get(color_name, BLUE)
    img = image.copy()
    overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
    overlay.fill((*overlay_color, 85))
    img.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return img


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        original = load_image("Player.png", (45, 85))
        self.image = recolor_car(original, color_name)
        self.rect = self.image.get_rect(center=(LANES[1], 510))
        self.speed = 6

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.move_ip(-self.speed, 0)
        if pressed[K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip(self.speed, 0)
        if pressed[K_UP] and self.rect.top > 80:
            self.rect.move_ip(0, -self.speed)
        if pressed[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT - 10:
            self.rect.move_ip(0, self.speed)


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, speed, player_rect):
        super().__init__()
        self.image = load_image("Enemy.png", (45, 85))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.respawn(player_rect)

    def respawn(self, player_rect):
        for _ in range(20):
            self.rect.centerx = random.choice(LANES)
            self.rect.y = random.randint(-700, -80)
            if abs(self.rect.centerx - player_rect.centerx) > 50 or self.rect.y < -150:
                return
        self.rect.centerx = random.choice(LANES)
        self.rect.y = -250

    def update(self, player_rect):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn(player_rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = load_image("Coin.png", (32, 32))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.value = 1
        self.respawn()

    def respawn(self):
        self.value = random.choice([1, 1, 1, 2, 3])
        size = 28 + self.value * 5
        self.image = load_image("Coin.png", (size, size))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = random.randint(-650, -60)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, player_rect):
        super().__init__()
        self.kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])
        self.image = self.make_image()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.respawn(player_rect)

    def make_image(self):
        surf = pygame.Surface((55, 35), pygame.SRCALPHA)
        if self.kind == "barrier":
            pygame.draw.rect(surf, ORANGE, (0, 8, 55, 20), border_radius=5)
            pygame.draw.line(surf, BLACK, (5, 12), (50, 28), 4)
            pygame.draw.line(surf, BLACK, (50, 12), (5, 28), 4)
        elif self.kind == "oil":
            pygame.draw.ellipse(surf, BLACK, (5, 5, 45, 25))
            pygame.draw.ellipse(surf, DARK_GRAY, (12, 8, 25, 12))
        elif self.kind == "pothole":
            pygame.draw.ellipse(surf, BROWN, (4, 5, 47, 25))
            pygame.draw.ellipse(surf, BLACK, (10, 10, 30, 12))
        else:
            pygame.draw.rect(surf, YELLOW, (3, 12, 50, 14), border_radius=6)
            pygame.draw.rect(surf, BLACK, (3, 12, 50, 14), 2, border_radius=6)
        return surf

    def respawn(self, player_rect):
        self.kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])
        self.image = self.make_image()
        self.rect = self.image.get_rect()
        for _ in range(20):
            self.rect.centerx = random.choice(LANES)
            self.rect.y = random.randint(-850, -90)
            if abs(self.rect.centerx - player_rect.centerx) > 50 or self.rect.y < -180:
                return
        self.rect.centerx = random.choice(LANES)
        self.rect.y = -300

    def update(self, player_rect):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn(player_rect)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.image = self.make_image()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.respawn()

    def make_image(self):
        surf = pygame.Surface((36, 36), pygame.SRCALPHA)
        if self.kind == "nitro":
            pygame.draw.circle(surf, PURPLE, (18, 18), 17)
            font = pygame.font.SysFont("Verdana", 18, bold=True)
            surf.blit(font.render("N", True, WHITE), (11, 6))
        elif self.kind == "shield":
            pygame.draw.circle(surf, BLUE, (18, 18), 17)
            pygame.draw.polygon(surf, WHITE, [(18, 5), (30, 12), (26, 29), (18, 34), (10, 29), (6, 12)])
        else:
            pygame.draw.circle(surf, GREEN, (18, 18), 17)
            pygame.draw.rect(surf, WHITE, (8, 15, 20, 6))
            pygame.draw.rect(surf, WHITE, (15, 8, 6, 20))
        return surf

    def respawn(self):
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.image = self.make_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = random.randint(-1200, -300)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.move_ip(0, self.speed)
        age = pygame.time.get_ticks() - self.spawn_time
        if self.rect.top > SCREEN_HEIGHT or age > 7000:
            self.respawn()


class MovingBarrier(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((70, 25), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, 70, 25), border_radius=5)
        pygame.draw.rect(self.image, WHITE, (8, 8, 16, 8))
        pygame.draw.rect(self.image, WHITE, (45, 8, 16, 8))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -500))
        self.speed = speed
        self.side_speed = random.choice([-2, 2])

    def update(self):
        self.rect.move_ip(self.side_speed, self.speed)
        if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
            self.side_speed *= -1
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.centerx = random.choice(LANES)
            self.rect.y = random.randint(-1400, -600)


class RacerGame:
    def __init__(self, screen, clock, settings, username):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.username = username
        self.font = pygame.font.SysFont("Verdana", 18)
        self.big_font = pygame.font.SysFont("Verdana", 48)
        self.background = pygame.image.load(os.path.join(ASSET_DIR, "AnimatedStreet.png")).convert()
        self.crash_sound = None
        if settings.get("sound", True):
            try:
                self.crash_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "crash.wav"))
            except pygame.error:
                self.crash_sound = None
        self.reset()

    def reset(self):
        difficulty = self.settings.get("difficulty", "normal")
        if difficulty == "easy":
            self.base_speed = 4
            traffic_count = 1
            obstacle_count = 2
        elif difficulty == "hard":
            self.base_speed = 7
            traffic_count = 3
            obstacle_count = 4
        else:
            self.base_speed = 5
            traffic_count = 2
            obstacle_count = 3

        self.speed = self.base_speed
        self.player = Player(self.settings.get("car_color", "blue"))
        self.traffic = pygame.sprite.Group(*[TrafficCar(self.speed, self.player.rect) for _ in range(traffic_count)])
        self.coins_group = pygame.sprite.Group(Coin(self.speed))
        self.obstacles = pygame.sprite.Group(*[Obstacle(self.speed, self.player.rect) for _ in range(obstacle_count)])
        self.powerups = pygame.sprite.Group(PowerUp(self.speed))
        self.events = pygame.sprite.Group(MovingBarrier(self.speed))
        self.coins = 0
        self.score = 0
        self.distance = 0
        self.active_power = None
        self.power_end_time = 0
        self.has_shield = False
        self.finished = False
        self.game_over = False
        self.saved = False

    def apply_speed_to_objects(self):
        for group in [self.traffic, self.coins_group, self.obstacles, self.powerups, self.events]:
            for sprite in group:
                sprite.speed = self.speed

    def activate_powerup(self, kind):
        self.active_power = kind
        now = pygame.time.get_ticks()
        if kind == "nitro":
            self.power_end_time = now + 4000
            self.speed += 3
        elif kind == "shield":
            self.has_shield = True
            self.power_end_time = 0
        elif kind == "repair":
            if len(self.obstacles) > 0:
                random.choice(self.obstacles.sprites()).respawn(self.player.rect)
            self.active_power = None
            self.score += 30
        self.apply_speed_to_objects()

    def update_active_power(self):
        if self.active_power == "nitro" and pygame.time.get_ticks() > self.power_end_time:
            self.active_power = None
            self.speed = self.base_speed + self.distance // 700
            self.apply_speed_to_objects()

    def handle_crash(self):
        if self.has_shield:
            self.has_shield = False
            self.active_power = None
            for sprite in list(self.traffic) + list(self.obstacles) + list(self.events):
                if self.player.rect.colliderect(sprite.rect):
                    if hasattr(sprite, "respawn"):
                        sprite.respawn(self.player.rect)
                    else:
                        sprite.rect.y = -700
            return
        if self.crash_sound:
            self.crash_sound.play()
        self.game_over = True

    def calculate_score(self):
        self.score = self.coins * 20 + int(self.distance * 0.3)
        if self.active_power == "nitro":
            self.score += 50
        if self.finished:
            self.score += 500

    def draw_hud(self):
        remaining = max(0, FINISH_DISTANCE - int(self.distance))
        items = [
            f"Name: {self.username}",
            f"Score: {int(self.score)}",
            f"Coins: {self.coins}",
            f"Distance: {int(self.distance)}m",
            f"Left: {remaining}m"
        ]
        y = 8
        for text in items:
            surf = self.font.render(text, True, BLACK)
            self.screen.blit(surf, (8, y))
            y += 22

        power_text = "Power: None"
        if self.active_power == "nitro":
            sec = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
            power_text = f"Power: Nitro {sec}s"
        elif self.active_power == "shield":
            power_text = "Power: Shield"
        surf = self.font.render(power_text, True, BLACK)
        self.screen.blit(surf, (210, 8))

    def draw_finish_line(self):
        if FINISH_DISTANCE - self.distance < 500:
            y = int(80 + (FINISH_DISTANCE - self.distance))
            if -50 < y < SCREEN_HEIGHT:
                pygame.draw.rect(self.screen, WHITE, (ROAD_LEFT, y, ROAD_RIGHT - ROAD_LEFT, 16))
                for i in range(ROAD_LEFT, ROAD_RIGHT, 40):
                    pygame.draw.rect(self.screen, BLACK, (i, y, 20, 16))

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

            self.player.move()
            self.update_active_power()

            if self.active_power != "nitro":
                self.speed = self.base_speed + self.distance // 700
                self.apply_speed_to_objects()

            for traffic in self.traffic:
                traffic.update(self.player.rect)
            for coin in self.coins_group:
                coin.update()
            for obstacle in self.obstacles:
                obstacle.update(self.player.rect)
            for powerup in self.powerups:
                powerup.update()
            for event in self.events:
                event.update()

            collected_coin = pygame.sprite.spritecollideany(self.player, self.coins_group)
            if collected_coin:
                self.coins += collected_coin.value
                self.score += collected_coin.value * 20
                collected_coin.respawn()

            collected_power = pygame.sprite.spritecollideany(self.player, self.powerups)
            if collected_power and self.active_power is None:
                self.activate_powerup(collected_power.kind)
                collected_power.respawn()

            if pygame.sprite.spritecollideany(self.player, self.traffic):
                self.handle_crash()
            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                hit = pygame.sprite.spritecollideany(self.player, self.obstacles)
                if hit.kind in ["oil", "speed_bump"]:
                    self.speed = max(2, self.speed - 1)
                    hit.respawn(self.player.rect)
                else:
                    self.handle_crash()
            if pygame.sprite.spritecollideany(self.player, self.events):
                self.handle_crash()

            self.distance += self.speed * 0.12
            if self.distance >= FINISH_DISTANCE:
                self.finished = True
                self.game_over = True

            self.calculate_score()

            self.screen.blit(self.background, (0, 0))
            self.draw_finish_line()
            for group in [self.coins_group, self.powerups, self.obstacles, self.events, self.traffic]:
                group.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            self.draw_hud()

            pygame.display.update()
            self.clock.tick(60)

        if not self.saved:
            save_score(self.username, self.score, self.distance, self.coins)
            self.saved = True
        return "game_over", int(self.score), int(self.distance), self.coins, self.finished

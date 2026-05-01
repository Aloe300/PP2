import os
import pygame
from ui import Button, draw_center_text, ask_username
from persistence import load_settings, save_settings, load_leaderboard
from racer import RacerGame, SCREEN_WIDTH, SCREEN_HEIGHT


def main_menu(screen, clock):
    font_big = pygame.font.SysFont("Verdana", 42)
    font = pygame.font.SysFont("Verdana", 24)
    buttons = [
        Button(100, 170, 200, 55, "Play", font),
        Button(100, 245, 200, 55, "Leaderboard", font),
        Button(100, 320, 200, 55, "Settings", font),
        Button(100, 395, 200, 55, "Quit", font),
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if buttons[0].clicked(event):
                return "play"
            if buttons[1].clicked(event):
                return "leaderboard"
            if buttons[2].clicked(event):
                return "settings"
            if buttons[3].clicked(event):
                return "quit"
        screen.fill((35, 35, 35))
        draw_center_text(screen, "RACER", font_big, (255, 255, 255), 95)
        for button in buttons:
            button.draw(screen)
        pygame.display.update()
        clock.tick(60)


def leaderboard_screen(screen, clock):
    font_big = pygame.font.SysFont("Verdana", 34)
    font = pygame.font.SysFont("Verdana", 18)
    small = pygame.font.SysFont("Verdana", 15)
    back = Button(125, 520, 150, 45, "Back", font)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if back.clicked(event):
                return "menu"
        screen.fill((30, 30, 30))
        draw_center_text(screen, "TOP 10", font_big, (255, 255, 255), 55)
        leaderboard = load_leaderboard()
        if not leaderboard:
            draw_center_text(screen, "No scores yet", font, (255, 255, 255), 180)
        else:
            y = 115
            header = small.render("Rank  Name        Score    Dist", True, (255, 255, 0))
            screen.blit(header, (35, 90))
            for i, item in enumerate(leaderboard[:10], start=1):
                line = f"{i:<5} {item.get('name', 'Player')[:10]:<10} {item.get('score', 0):<8} {item.get('distance', 0)}m"
                surf = small.render(line, True, (255, 255, 255))
                screen.blit(surf, (35, y))
                y += 35
        back.draw(screen)
        pygame.display.update()
        clock.tick(60)


def settings_screen(screen, clock, settings):
    font_big = pygame.font.SysFont("Verdana", 32)
    font = pygame.font.SysFont("Verdana", 18)
    sound_btn = Button(70, 130, 260, 45, "", font)
    color_btn = Button(70, 205, 260, 45, "", font)
    diff_btn = Button(70, 280, 260, 45, "", font)
    back_btn = Button(125, 470, 150, 45, "Back", font)
    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    def update_text():
        sound_btn.text = "Sound: ON" if settings.get("sound", True) else "Sound: OFF"
        color_btn.text = f"Car color: {settings.get('car_color', 'blue')}"
        diff_btn.text = f"Difficulty: {settings.get('difficulty', 'normal')}"

    while True:
        update_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings)
                return "menu"
            if sound_btn.clicked(event):
                settings["sound"] = not settings.get("sound", True)
                save_settings(settings)
            if color_btn.clicked(event):
                current = settings.get("car_color", "blue")
                settings["car_color"] = colors[(colors.index(current) + 1) % len(colors)] if current in colors else "blue"
                save_settings(settings)
            if diff_btn.clicked(event):
                current = settings.get("difficulty", "normal")
                settings["difficulty"] = difficulties[(difficulties.index(current) + 1) % len(difficulties)] if current in difficulties else "normal"
                save_settings(settings)
            if back_btn.clicked(event):
                save_settings(settings)
                return "menu"

        screen.fill((35, 35, 35))
        draw_center_text(screen, "SETTINGS", font_big, (255, 255, 255), 70)
        for button in [sound_btn, color_btn, diff_btn, back_btn]:
            button.draw(screen)
        hint = font.render("Click buttons to change settings", True, (255, 255, 255))
        screen.blit(hint, (55, 370))
        pygame.display.update()
        clock.tick(60)


def game_over_screen(screen, clock, result):
    _, score, distance, coins, finished = result
    font_big = pygame.font.SysFont("Verdana", 36)
    font = pygame.font.SysFont("Verdana", 20)
    retry = Button(75, 390, 110, 50, "Retry", font)
    menu = Button(205, 390, 130, 50, "Main Menu", font)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if retry.clicked(event):
                return "retry"
            if menu.clicked(event):
                return "menu"
        screen.fill((120, 30, 30))
        title = "FINISHED!" if finished else "GAME OVER"
        draw_center_text(screen, title, font_big, (255, 255, 255), 110)
        lines = [f"Score: {score}", f"Distance: {distance}m", f"Coins: {coins}"]
        y = 190
        for line in lines:
            draw_center_text(screen, line, font, (255, 255, 255), y)
            y += 45
        retry.draw(screen)
        menu.draw(screen)
        pygame.display.update()
        clock.tick(60)


def run_game(screen, clock, settings):
    username = ask_username(screen, clock)
    if not username:
        return "menu"
    while True:
        game = RacerGame(screen, clock, settings, username)
        result = game.run()
        if result == "quit":
            return "quit"
        if result == "menu":
            return "menu"
        action = game_over_screen(screen, clock, result)
        if action == "retry":
            continue
        return action


def main():
    os.environ.setdefault("SDL_VIDEO_CENTERED", "1")
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Racer Advanced")
    clock = pygame.time.Clock()
    settings = load_settings()

    while True:
        action = main_menu(screen, clock)
        if action == "quit":
            break
        if action == "play":
            result = run_game(screen, clock, settings)
            if result == "quit":
                break
        elif action == "leaderboard":
            result = leaderboard_screen(screen, clock)
            if result == "quit":
                break
        elif action == "settings":
            result = settings_screen(screen, clock, settings)
            settings = load_settings()
            if result == "quit":
                break
    pygame.quit()


if __name__ == "__main__":
    main()

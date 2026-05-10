import time
from pathlib import Path

import pygame


WIDTH = 800
HEIGHT = 440
FPS = 30

WHITE = (245, 245, 245)
BLACK = (25, 25, 25)
BLUE = (70, 120, 220)
GRAY = (130, 130, 130)
GREEN = (40, 150, 70)


class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = Path(music_folder)
        self.tracks = self.load_tracks()
        self.current_index = 0
        self.current_position = 0.0
        self.last_resume_time = None
        self.is_playing = False
        self.is_paused = False

    def load_tracks(self):
        tracks = []
        for file_path in sorted(self.music_folder.iterdir()):
            if file_path.suffix.lower() in [".mp3", ".wav", ".ogg"]:
                tracks.append(file_path)
        return tracks

    def has_tracks(self):
        return len(self.tracks) > 0

    def get_current_track(self):
        if not self.has_tracks():
            return None
        return self.tracks[self.current_index]

    def play(self):
        if not self.has_tracks():
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.last_resume_time = time.time()
            self.is_paused = False
            self.is_playing = True
            return

        if self.is_playing:
            return

        current_track = self.get_current_track()
        pygame.mixer.music.load(str(current_track))
        pygame.mixer.music.play()
        self.current_position = 0.0
        self.last_resume_time = time.time()
        self.is_playing = True
        self.is_paused = False

    def stop(self):
        if not self.is_playing or self.is_paused:
            return

        pygame.mixer.music.pause()
        self.current_position += time.time() - self.last_resume_time
        self.last_resume_time = None
        self.is_paused = True

    def next_track(self):
        if not self.has_tracks():
            return
        pygame.mixer.music.stop()
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.current_position = 0.0
        self.last_resume_time = None
        self.is_playing = False
        self.is_paused = False
        self.play()

    def previous_track(self):
        if not self.has_tracks():
            return
        pygame.mixer.music.stop()
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.current_position = 0.0
        self.last_resume_time = None
        self.is_playing = False
        self.is_paused = False
        self.play()

    def get_elapsed_seconds(self):
        if self.is_playing and not self.is_paused and self.last_resume_time is not None:
            return int(self.current_position + (time.time() - self.last_resume_time))
        return int(self.current_position)

    def get_status_text(self):
        if self.is_paused:
            return "Paused"
        if self.is_playing:
            return "Playing"
        return "Stopped"

    def update(self):
        if self.is_playing and not self.is_paused and not pygame.mixer.music.get_busy():
            self.current_position = 0.0
            self.last_resume_time = None
            self.is_playing = False

    def close(self):
        pygame.mixer.music.stop()
        self.current_position = 0.0
        self.last_resume_time = None
        self.is_playing = False
        self.is_paused = False


class MusicPlayerApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Music Player")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("arial", 36, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 22)

        base_path = Path(__file__).resolve().parent
        self.player = MusicPlayer(base_path / "music")

    def draw(self):
        self.screen.fill(WHITE)

        title = self.title_font.render("Keyboard Music Player", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        if self.player.has_tracks():
            current_track = self.player.get_current_track()
            name_surface = self.text_font.render(f"Current track: {current_track.name}", True, BLUE)
            self.screen.blit(name_surface, (60, 110))

            elapsed = self.player.get_elapsed_seconds()
            progress_surface = self.text_font.render(f"Playback: {elapsed} sec", True, GREEN)
            self.screen.blit(progress_surface, (60, 160))

            status_surface = self.small_font.render(
                f"Status: {self.player.get_status_text()}",
                True,
                BLACK,
            )
            self.screen.blit(status_surface, (60, 205))

            playlist_surface = self.small_font.render(
                f"Track {self.player.current_index + 1} of {len(self.player.tracks)}",
                True,
                BLACK,
            )
            self.screen.blit(playlist_surface, (60, 235))
        else:
            warning = self.text_font.render("No music files found in music/ folder", True, BLUE)
            self.screen.blit(warning, (60, 135))

        help_lines = [
            "P - play / resume",
            "S - pause",
            "N - next track",
            "B - previous track",
            "Q - quit",
        ]

        top = 290
        for line in help_lines:
            surface = self.small_font.render(line, True, GRAY)
            self.screen.blit(surface, (60, top))
            top += 28

    def run(self):
        running = True

        while running:
            self.player.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_p:
                        self.player.play()
                    elif event.key == pygame.K_s:
                        self.player.stop()
                    elif event.key == pygame.K_n:
                        self.player.next_track()
                    elif event.key == pygame.K_b:
                        self.player.previous_track()

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        self.player.close()
        pygame.quit()

import os
from datetime import datetime

import pygame


class Mickeysclock:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "images")

        self.background = pygame.image.load(
            os.path.join(images_dir, "clock_itself.png")
        )

        self.minute_hand = pygame.image.load(
            os.path.join(images_dir, "right_hand.png")
        )

        self.second_hand = pygame.image.load(
            os.path.join(images_dir, "left_hand.png")
        )

        self.minute_hand = pygame.transform.smoothscale(
            self.minute_hand,
            (self.minute_hand.get_width() // 2, self.minute_hand.get_height() // 2)
        )

        self.second_hand = pygame.transform.smoothscale(
            self.second_hand,
            (self.second_hand.get_width() // 2, self.second_hand.get_height() // 2)
        )

        self.screen = None
        self.width = self.background.get_width()
        self.height = self.background.get_height()
        self.center = (self.width // 2, self.height // 2)

        self.font = None
        self.text_color = (255, 255, 255)

        self.minute_anchor = (20, self.minute_hand.get_height() - 20)
        self.second_anchor = (135, self.second_hand.get_height() - 18)

        self.base_angle = -90

    def set_screen(self, screen):
        self.screen = screen
        self.background = self.background.convert_alpha()
        self.minute_hand = self.minute_hand.convert_alpha()
        self.second_hand = self.second_hand.convert_alpha()

        self.font = pygame.font.SysFont("arial", 34, bold=True)

    def blit_rotate(self, image, pivot, anchor, angle):
        image_rect = image.get_rect(
            topleft=(pivot[0] - anchor[0], pivot[1] - anchor[1])
        )

        offset = pygame.math.Vector2(pivot) - image_rect.center
        rotated_offset = offset.rotate(angle)

        rotated_center = (
            pivot[0] - rotated_offset.x,
            pivot[1] - rotated_offset.y
        )

        rotated_image = pygame.transform.rotozoom(image, -angle, 1)
        rotated_rect = rotated_image.get_rect(center=rotated_center)

        self.screen.blit(rotated_image, rotated_rect)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        now = datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = self.base_angle + (minutes + seconds / 60) * 6
        second_angle = self.base_angle + seconds * 6

        self.blit_rotate(self.minute_hand, self.center, self.minute_anchor, minute_angle)
        self.blit_rotate(self.second_hand, self.center, self.second_anchor, second_angle)

        time_text = self.font.render(
            f"{now.hour:02d}:{minutes:02d}",
            True,
            self.text_color
        )
        text_rect = time_text.get_rect(center=(self.width // 2, 40))
        self.screen.blit(time_text, text_rect)

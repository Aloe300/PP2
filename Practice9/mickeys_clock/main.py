import pygame

from clock import Mickeysclock


def main():
    pygame.init()

    app = Mickeysclock()
    screen = pygame.display.set_mode((app.width, app.height))
    pygame.display.set_caption("Mickey's clock")

    app.set_screen(screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        app.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

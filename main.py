# main.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com
# https://kawerifytech.com

import pygame
import sys
from game import Game


def main() -> None:
    pygame.init()
    pygame.mixer.init(frequency=44_100, size=-16, channels=2, buffer=512)

    screen = pygame.display.set_mode(
        (1280, 720),
        pygame.DOUBLEBUF | pygame.HWSURFACE,
    )
    pygame.display.set_caption("My Python Pong — KawerifyTech")

    # Programmatic icon: glowing ball
    icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(icon, (0, 80, 100),  (16, 16), 16)   # outer glow
    pygame.draw.circle(icon, (0, 230, 255), (16, 16), 13)   # ball colour
    pygame.draw.circle(icon, (5, 5, 18),    (16, 16),  8)   # dark core
    pygame.draw.circle(icon, (0, 230, 255), (16, 16),  4)   # bright centre
    pygame.draw.circle(icon, (255, 255, 255),(13, 12),  2)   # specular
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    game  = Game(screen)

    while True:
        dt     = clock.tick(60)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.handle_events(events)
        game.update(dt)
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()

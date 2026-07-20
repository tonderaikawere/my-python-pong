# powerup.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import pygame
import random
import math
from constants import *

# ── Power-up catalogue ────────────────────────────────────────────────────────
POWERUP_TYPES = [
    "enlarge",     # collector's paddle grows
    "shrink_opp",  # opponent's paddle shrinks
    "speed_up",    # ball accelerates
    "slow_down",   # ball decelerates
    "multi_ball",  # extra ball spawned
]

_COLORS = {
    "enlarge"   : NEON_GREEN,
    "shrink_opp": NEON_PINK,
    "speed_up"  : NEON_YELLOW,
    "slow_down" : NEON_CYAN,
    "multi_ball": NEON_PURPLE,
}

_LABELS = {
    "enlarge"   : "+",
    "shrink_opp": "-",
    "speed_up"  : "!",
    "slow_down" : "~",
    "multi_ball": "x",
}

_DESCS = {
    "enlarge"   : "BIG",
    "shrink_opp": "SHRINK",
    "speed_up"  : "FAST",
    "slow_down" : "SLOW",
    "multi_ball": "2x",
}


class PowerUp:
    """A floating collectible that applies an effect when hit by the ball."""

    def __init__(self):
        self.kind  = random.choice(POWERUP_TYPES)
        self.color = _COLORS[self.kind]
        self.label = _LABELS[self.kind]
        self.desc  = _DESCS[self.kind]
        self.x     = random.randint(WIDTH  // 4, 3 * WIDTH  // 4)
        self.y     = random.randint(90,           HEIGHT - 90)
        self.size  = POWERUP_SIZE
        self.alive = True
        self.pulse = 0.0
        self._font  = None

    def _get_font(self) -> pygame.font.Font:
        if self._font is None:
            for name in ("Orbitron", "Segoe UI", "Arial"):
                try:
                    self._font = pygame.font.SysFont(name, 13, bold=True)
                    break
                except Exception:
                    pass
            if self._font is None:
                self._font = pygame.font.Font(None, 16)
        return self._font

    def update(self, dt: int) -> None:
        self.pulse += dt * 0.006

    @property
    def rect(self) -> pygame.Rect:
        h = self.size // 2
        return pygame.Rect(self.x - h, self.y - h, self.size, self.size)

    def draw(self, surf: pygame.Surface) -> None:
        # Pulsing outer glow
        pr = int(self.size + math.sin(self.pulse) * 5)
        for r in range(pr + 16, pr, -4):
            a = max(0, int(70 * (r - pr) / 16))
            gs = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(gs, (*self.color, a), (r, r), r)
            surf.blit(gs, (self.x - r, self.y - r))

        # Body
        pygame.draw.circle(surf, self.color, (self.x, self.y), self.size // 2)
        pygame.draw.circle(surf, WHITE,      (self.x, self.y), self.size // 2, 2)

        # Label
        font  = self._get_font()
        label = font.render(self.desc, True, WHITE)
        surf.blit(label, (self.x - label.get_width() // 2,
                          self.y - label.get_height() // 2))


class PowerUpManager:
    """Spawns and manages active power-ups."""

    def __init__(self):
        self.active: list[PowerUp] = []
        self._timer = POWERUP_INTERVAL

    def update(self, dt: int) -> None:
        self._timer -= dt
        if self._timer <= 0:
            self._timer = POWERUP_INTERVAL
            if len(self.active) < 3:
                self.active.append(PowerUp())

        for pu in self.active:
            pu.update(dt)
        self.active = [p for p in self.active if p.alive]

    def check_collect(self, ball_rect: pygame.Rect) -> "PowerUp | None":
        for pu in self.active:
            if pu.alive and pu.rect.colliderect(ball_rect):
                pu.alive = False
                return pu
        return None

    def draw(self, surf: pygame.Surface) -> None:
        for pu in self.active:
            pu.draw(surf)

    def reset(self) -> None:
        self.active = []
        self._timer = POWERUP_INTERVAL

# ball.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import pygame
import math
import random
from constants import *


class Ball:
    """Pong ball with trail, glow, and physics."""

    def __init__(self, x=None, y=None, vx=None, vy=None):
        self.x  = float(x if x is not None else WIDTH  // 2)
        self.y  = float(y if y is not None else HEIGHT // 2)
        sx      = random.choice([-1, 1])
        sy      = random.choice([-1, 1])
        self.vx = float(vx if vx is not None else sx * BALL_INIT_SPEED)
        self.vy = float(vy if vy is not None else sy * BALL_INIT_SPEED * random.uniform(0.45, 0.85))

        self.trail       : list[tuple[float, float]] = []
        self.color       = NEON_CYAN
        self.glow_radius = BALL_SIZE * 3
        self.pulse       = 0.0  # animation phase

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self, dt: int) -> str | None:
        """Move the ball; returns 'wall' on top/bottom bounce, else None."""
        self.pulse += dt * 0.006

        # Record trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

        self.x += self.vx
        self.y += self.vy

        half = BALL_SIZE // 2
        if self.y - half <= 0:
            self.y   = float(half)
            self.vy  = abs(self.vy)
            return "wall"
        if self.y + half >= HEIGHT:
            self.y   = float(HEIGHT - half)
            self.vy  = -abs(self.vy)
            return "wall"
        return None

    # ── Reset ─────────────────────────────────────────────────────────────────
    def reset(self, direction: int = 1) -> None:
        self.x     = float(WIDTH  // 2)
        self.y     = float(HEIGHT // 2)
        self.vx    = float(direction * BALL_INIT_SPEED)
        self.vy    = float(random.choice([-1, 1]) * BALL_INIT_SPEED * random.uniform(0.45, 0.85))
        self.trail = []

    # ── Speed up after paddle hit ─────────────────────────────────────────────
    def speed_up(self) -> None:
        speed = math.hypot(self.vx, self.vy)
        if speed < BALL_MAX_SPEED:
            f       = (speed + BALL_SPEED_INC) / speed
            self.vx *= f
            self.vy *= f

    # ── Collision rect ────────────────────────────────────────────────────────
    @property
    def rect(self) -> pygame.Rect:
        h = BALL_SIZE // 2
        return pygame.Rect(int(self.x) - h, int(self.y) - h, BALL_SIZE, BALL_SIZE)

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self, surf: pygame.Surface) -> None:
        self._draw_trail(surf)
        self._draw_glow(surf)
        self._draw_core(surf)

    def _draw_trail(self, surf: pygame.Surface) -> None:
        n = max(len(self.trail), 1)
        for i, (tx, ty) in enumerate(self.trail):
            frac  = i / n
            alpha = int(200 * frac * 0.7)
            size  = max(2, int(BALL_SIZE * 0.55 * frac))
            ts    = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(ts, (*self.color, alpha), (size, size), size)
            surf.blit(ts, (int(tx) - size, int(ty) - size))

    def _draw_glow(self, surf: pygame.Surface) -> None:
        gr = int(self.glow_radius + math.sin(self.pulse) * 5)
        gs = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
        for r in range(gr, 0, -3):
            a = max(0, int(55 * (r / gr) ** 1.8))
            pygame.draw.circle(gs, (*self.color, a), (gr, gr), r)
        surf.blit(gs, (int(self.x) - gr, int(self.y) - gr))

    def _draw_core(self, surf: pygame.Surface) -> None:
        bx, by = int(self.x), int(self.y)
        pygame.draw.circle(surf, self.color, (bx, by), BALL_SIZE // 2)
        # Specular highlight
        pygame.draw.circle(surf, WHITE, (bx - 2, by - 3), max(2, BALL_SIZE // 5))

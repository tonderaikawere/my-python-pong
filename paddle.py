# paddle.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import pygame
import math
from constants import *


class Paddle:
    """Player or AI paddle with glow rendering and power-up states."""

    def __init__(self, side: str, color=None):
        self.side   = side   # 'left' | 'right'
        self.color  = color or (P1_COLOR if side == "left" else P2_COLOR)
        self.w      = PADDLE_W
        self.h      = PADDLE_H
        self.x      = float(PADDLE_MARGIN if side == "left"
                            else WIDTH - PADDLE_MARGIN - PADDLE_W)
        self.y      = float(HEIGHT // 2 - PADDLE_H // 2)
        self.speed  = PADDLE_SPEED
        self.vel_y  = 0.0
        self.pulse  = 0.0
        self.hit_flash = 0   # ms remaining for white hit-flash

        # Power-up state
        self.enlarged = False
        self.shrunk   = False
        self.pu_timer = 0

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self, dt: int) -> None:
        self.pulse += dt * 0.005
        self.hit_flash = max(0, self.hit_flash - dt)

        if self.enlarged or self.shrunk:
            self.pu_timer -= dt
            if self.pu_timer <= 0:
                self.h        = PADDLE_H
                self.enlarged = False
                self.shrunk   = False

        self.y += self.vel_y
        self.y  = max(0.0, min(float(HEIGHT - self.h), self.y))

    # ── Movement ──────────────────────────────────────────────────────────────
    def move_up(self)   -> None: self.vel_y = -self.speed
    def move_down(self) -> None: self.vel_y =  self.speed
    def stop(self)      -> None: self.vel_y =  0.0

    # ── Collision rect ────────────────────────────────────────────────────────
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    # ── Power-ups ─────────────────────────────────────────────────────────────
    def apply_enlarge(self) -> None:
        self.h        = int(PADDLE_H * 1.7)
        self.enlarged = True
        self.shrunk   = False
        self.pu_timer = POWERUP_DURATION

    def apply_shrink(self) -> None:
        self.h        = int(PADDLE_H * 0.55)
        self.shrunk   = True
        self.enlarged = False
        self.pu_timer = POWERUP_DURATION

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self, surf: pygame.Surface) -> None:
        self._draw_glow(surf)
        self._draw_body(surf)

    def _draw_glow(self, surf: pygame.Surface) -> None:
        r   = self.rect
        pad = 14
        gw  = self.w + pad * 2
        gh  = self.h + pad * 2
        gs  = pygame.Surface((gw, gh), pygame.SRCALPHA)
        # Brighter glow when moving, dimmer at rest
        base_a = int(abs(math.sin(self.pulse)) * 55 + 18)
        if self.vel_y != 0:
            base_a = min(110, base_a + 55)
        for i in range(5, 0, -1):
            pw = self.w + i * 4
            ph = self.h + i * 4
            ia = max(0, base_a - i * 7)
            pygame.draw.rect(
                gs, (*self.color, ia),
                ((gw - pw) // 2, (gh - ph) // 2, pw, ph),
                border_radius=7
            )
        surf.blit(gs, (r.x - pad, r.y - pad))

    def flash_hit(self) -> None:
        """Trigger a white flash on the paddle."""
        self.hit_flash = 120   # ms

    def _draw_body(self, surf: pygame.Surface) -> None:
        r     = self.rect
        color = WHITE if self.hit_flash > 80 else self.color
        pygame.draw.rect(surf, color, r, border_radius=7)
        # Inner highlight stripe
        hi = pygame.Surface((max(2, self.w - 6), max(6, self.h - 12)), pygame.SRCALPHA)
        hi.fill((255, 255, 255, 38))
        surf.blit(hi, (r.x + 3, r.y + 6))

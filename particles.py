# particles.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import pygame
import random
import math
from constants import *


class Particle:
    """Single particle with velocity, fade, and shrink-over-time."""

    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "size")

    def __init__(self, x: float, y: float, color: tuple):
        self.x        = float(x)
        self.y        = float(y)
        angle         = random.uniform(0, math.tau)
        speed         = random.uniform(1.0, 6.5)
        self.vx       = math.cos(angle) * speed
        self.vy       = math.sin(angle) * speed
        self.max_life = random.randint(25, 60)
        self.life     = self.max_life
        self.color    = color
        self.size     = random.uniform(2.0, 5.5)

    def update(self) -> None:
        self.x  += self.vx
        self.y  += self.vy
        self.vx *= 0.92
        self.vy *= 0.92
        self.vy += 0.08   # subtle gravity
        self.life -= 1

    @property
    def alive(self) -> bool:
        return self.life > 0

    def draw(self, surf: pygame.Surface) -> None:
        frac  = self.life / self.max_life
        alpha = int(255 * frac)
        size  = max(1, int(self.size * frac))
        s     = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (size, size), size)
        surf.blit(s, (int(self.x) - size, int(self.y) - size))


class ParticleSystem:
    """Manages a pool of particles."""

    def __init__(self):
        self.particles: list[Particle] = []

    def emit(self, x: float, y: float, color: tuple, count: int = 20) -> None:
        available = MAX_PARTICLES - len(self.particles)
        for _ in range(min(count, available)):
            self.particles.append(Particle(x, y, color))

    def emit_burst(self, x: float, y: float, color: tuple, count: int = 45) -> None:
        self.emit(x, y, color, count)

    def update(self) -> None:
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update()

    def draw(self, surf: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(surf)

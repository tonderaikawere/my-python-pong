# ai.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import random
from constants import *


class AIController:
    """
    Paddle AI with configurable difficulty.

    accuracy 0.0 → purely random
    accuracy 1.0 → perfect ball tracking + prediction
    """

    def __init__(self, accuracy: float = AI_MEDIUM):
        self.accuracy      = max(0.0, min(1.0, accuracy))
        self.target_y      = float(HEIGHT // 2)
        self._eval_timer   = 0       # ms until next re-evaluation
        self._return_bias  = 0.0     # small nudge toward center when idle

    # ── Update (called every frame) ───────────────────────────────────────────
    def update(self, paddle, balls: list, dt: int) -> None:
        self._eval_timer -= dt

        ball = self._pick_ball(balls)
        if ball is None:
            self._idle(paddle)
            return

        # Re-evaluate target periodically (lower accuracy → less frequent)
        interval = int(80 + (1 - self.accuracy) * 140)
        if self._eval_timer <= 0:
            self._eval_timer = random.randint(interval // 2, interval)
            predicted        = self._predict(ball)
            error            = (1 - self.accuracy) * random.uniform(
                                    -HEIGHT * 0.38, HEIGHT * 0.38)
            self.target_y    = predicted + error

        # Steer paddle toward target
        center = paddle.y + paddle.h / 2
        diff   = self.target_y - center
        speed  = paddle.speed
        if abs(diff) > 4:
            if diff > 0:
                paddle.vel_y = min(speed, abs(diff) * 0.25 + speed * 0.5) if self.accuracy > 0.7 else speed
                paddle.move_down()
            else:
                paddle.vel_y = min(speed, abs(diff) * 0.25 + speed * 0.5) if self.accuracy > 0.7 else speed
                paddle.move_up()
        else:
            paddle.stop()

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _pick_ball(self, balls: list):
        """Prefer balls moving toward the AI side (positive vx)."""
        if not balls:
            return None
        approaching = [b for b in balls if b.vx > 0]
        pool        = approaching if approaching else balls
        return min(pool, key=lambda b: abs(b.x - (WIDTH - PADDLE_MARGIN)))

    def _predict(self, ball) -> float:
        """Simulate ball path to estimate Y at the AI paddle's X position."""
        bx, by, vx, vy = ball.x, ball.y, ball.vx, ball.vy
        target_x = float(WIDTH - PADDLE_MARGIN - PADDLE_W)

        if vx <= 0:
            return float(HEIGHT // 2)   # ball moving away → return to centre

        steps = (target_x - bx) / vx
        py    = by + vy * steps

        # Bounce clamping
        half = BALL_SIZE // 2
        lo   = float(half)
        hi   = float(HEIGHT - half)
        # Fold the position within bounds
        span = hi - lo
        if span > 0:
            py = lo + abs((py - lo) % (2 * span) - span)

        return py

    def _idle(self, paddle) -> None:
        """Drift back to centre when no ball is available."""
        centre = HEIGHT // 2
        pad_c  = paddle.y + paddle.h / 2
        if abs(pad_c - centre) > 10:
            paddle.move_up() if pad_c > centre else paddle.move_down()
        else:
            paddle.stop()

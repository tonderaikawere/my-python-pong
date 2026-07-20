# game.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import pygame
import math
import random
from constants import *
from ball import Ball
from paddle import Paddle
from particles import ParticleSystem
from audio import AudioManager
from ai import AIController
from powerup import PowerUpManager
from ui import UIManager


class Game:
    """
    Top-level game object.
    Owns all subsystems and drives the state machine:
        SPLASH → MENU → MODE → PLAYING ⇌ PAUSED → WIN → MENU
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.W, self.H = screen.get_size()

        # Sub-systems
        self.ui        = UIManager(screen)
        self.audio     = AudioManager()
        self.particles = ParticleSystem()
        self.pu_mgr    = PowerUpManager()

        # State
        self.state     = STATE_SPLASH
        self.mode      = "1p"       # "1p" | "2p"
        self.diff_sel  = 1          # 0=easy 1=med 2=hard
        self.menu_sel  = 0

        # Match data
        self.score   = [0, 0]
        self.hits    = [0, 0]
        self.winner  = ""

        # Objects
        self.balls:   list[Ball]   = []
        self.paddles: list[Paddle] = []
        self.ai:      AIController | None = None

        # Effects
        self.shake        = 0      # frames of screen shake remaining
        self.hint_timer   = 4_000  # ms to show controls hint

        # Static background surface (grid + bg)
        self._bg = pygame.Surface((self.W, self.H))
        self._build_bg()

    # ── Background ────────────────────────────────────────────────────────────
    def _build_bg(self) -> None:
        self._bg.fill(BG_COLOR)
        for x in range(0, self.W, 80):
            pygame.draw.line(self._bg, GRID_COLOR, (x, 0), (x, self.H))
        for y in range(0, self.H, 80):
            pygame.draw.line(self._bg, GRID_COLOR, (0, y), (self.W, y))

    # ── Game start / reset ────────────────────────────────────────────────────
    def _start(self) -> None:
        self.paddles   = [Paddle("left"), Paddle("right")]
        self.balls     = [Ball()]
        self.score     = [0, 0]
        self.hits      = [0, 0]
        self.particles = ParticleSystem()
        self.pu_mgr.reset()
        self.hint_timer = 4_000
        self.shake      = 0

        _diff = {0: AI_EASY, 1: AI_MEDIUM, 2: AI_HARD}
        self.ai = AIController(_diff[self.diff_sel]) if self.mode == "1p" else None

        self.state = STATE_PLAYING

    # ── Input ─────────────────────────────────────────────────────────────────
    def handle_events(self, events: list) -> None:
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                self._key(ev.key)

    def _key(self, key: int) -> None:
        # ── Splash ──
        if self.state == STATE_SPLASH:
            self.state = STATE_MENU

        # ── Menu ──
        elif self.state == STATE_MENU:
            if key == pygame.K_UP:
                self.menu_sel = (self.menu_sel - 1) % 3
                self.audio.play("menu")
            elif key == pygame.K_DOWN:
                self.menu_sel = (self.menu_sel + 1) % 3
                self.audio.play("menu")
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self._menu_confirm()

        # ── Difficulty ──
        elif self.state == STATE_MODE:
            if key == pygame.K_UP:
                self.diff_sel = (self.diff_sel - 1) % 3
                self.audio.play("menu")
            elif key == pygame.K_DOWN:
                self.diff_sel = (self.diff_sel + 1) % 3
                self.audio.play("menu")
            elif key == pygame.K_RETURN:
                self._start()
            elif key == pygame.K_ESCAPE:
                self.state = STATE_MENU

        # ── Playing ──
        elif self.state == STATE_PLAYING:
            if   key == pygame.K_p: self.state = STATE_PAUSED
            elif key == pygame.K_r: self._start()
            elif key == pygame.K_m: self.state = STATE_MENU
            elif key == pygame.K_s: self.audio.toggle()

        # ── Paused ──
        elif self.state == STATE_PAUSED:
            if   key == pygame.K_p: self.state = STATE_PLAYING
            elif key == pygame.K_r: self._start()
            elif key == pygame.K_m: self.state = STATE_MENU
            elif key == pygame.K_s: self.audio.toggle()

        # ── Win ──
        elif self.state == STATE_WIN:
            if   key in (pygame.K_RETURN, pygame.K_SPACE): self._start()
            elif key == pygame.K_m: self.state = STATE_MENU

    def _menu_confirm(self) -> None:
        import sys
        if   self.menu_sel == 0: self.mode = "1p"; self.state = STATE_MODE
        elif self.menu_sel == 1: self.mode = "2p"; self._start()
        elif self.menu_sel == 2: pygame.quit(); sys.exit()

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self, dt: int) -> None:
        self.ui.update(dt)
        if self.shake > 0:
            self.shake -= 1
        if self.state == STATE_PLAYING:
            self._update_play(dt)

    def _update_play(self, dt: int) -> None:
        p1, p2 = self.paddles
        keys   = pygame.key.get_pressed()

        # P1 input (W/S)
        if   keys[pygame.K_w]: p1.move_up()
        elif keys[pygame.K_s]: p1.move_down()
        else:                  p1.stop()

        # P2 or AI
        if self.mode == "2p":
            if   keys[pygame.K_UP]:   p2.move_up()
            elif keys[pygame.K_DOWN]: p2.move_down()
            else:                     p2.stop()
        else:
            self.ai.update(p2, self.balls, dt)

        p1.update(dt)
        p2.update(dt)

        scored = self._update_balls(dt)
        self.particles.update()
        self.pu_mgr.update(dt)
        self.hint_timer = max(0, self.hint_timer - dt)

        # Check win condition
        for i, sc in enumerate(self.score):
            if sc >= WIN_SCORE:
                self.winner = f"Player {i + 1}"
                self.audio.play("win")
                self.state  = STATE_WIN
                break

    def _update_balls(self, dt: int) -> bool:
        p1, p2 = self.paddles
        to_remove = []

        for ball in self.balls:
            result = ball.update(dt)
            if result == "wall":
                self.audio.play("wall")
                self.particles.emit(int(ball.x), int(ball.y), NEON_CYAN, 12)

            # Paddle hits
            for idx, pad in enumerate((p1, p2)):
                if ball.rect.colliderect(pad.rect):
                    self._paddle_hit(ball, pad, idx)

            # Power-up collection
            pu = self.pu_mgr.check_collect(ball.rect)
            if pu:
                self._apply_pu(pu, ball)

            # Scoring
            if ball.x < 0:
                self._do_score(1, ball.y, P2_COLOR)
                to_remove.append(ball)
            elif ball.x > self.W:
                self._do_score(0, ball.y, P1_COLOR)
                to_remove.append(ball)

        for b in to_remove:
            if b in self.balls:
                self.balls.remove(b)

        # Always keep at least one ball
        if not self.balls:
            d = 1 if sum(self.score) % 2 == 0 else -1
            nb = Ball()
            nb.reset(d)
            self.balls.append(nb)

        return bool(to_remove)

    def _do_score(self, scorer: int, ball_y: float, color: tuple) -> None:
        self.score[scorer] += 1
        self.ui.flash_score(scorer)
        self.audio.play("score")
        wall_x = self.W if scorer == 0 else 0
        self.particles.emit_burst(wall_x, int(ball_y), color, 55)
        self.shake = 14

    def _paddle_hit(self, ball: Ball, pad: Paddle, idx: int) -> None:
        # Positional correction
        if idx == 0:    # left paddle
            ball.vx = abs(ball.vx)
            ball.x  = float(pad.rect.right + BALL_SIZE // 2 + 1)
        else:           # right paddle
            ball.vx = -abs(ball.vx)
            ball.x  = float(pad.rect.left  - BALL_SIZE // 2 - 1)

        # Spin based on contact point
        rel_y  = (ball.y - (pad.y + pad.h / 2)) / (pad.h / 2)
        ball.vy = rel_y * abs(ball.vx) * 0.85
        ball.speed_up()

        self.hits[idx] += 1
        self.audio.play("hit")
        col = P1_COLOR if idx == 0 else P2_COLOR
        self.particles.emit(int(ball.x), int(ball.y), col, 22)
        pad.flash_hit()   # white paddle flash

    def _apply_pu(self, pu, ball: Ball) -> None:
        collector = 0 if ball.vx < 0 else 1
        opponent  = 1 - collector
        self.audio.play("pu")

        if pu.kind == "enlarge":
            self.paddles[collector].apply_enlarge()
        elif pu.kind == "shrink_opp":
            self.paddles[opponent].apply_shrink()
        elif pu.kind == "speed_up":
            ball.vx *= 1.3
            ball.vy *= 1.3
        elif pu.kind == "slow_down":
            speed = math.hypot(ball.vx, ball.vy)
            f     = max(0.5, (speed - 2) / speed)
            ball.vx *= f
            ball.vy *= f
        elif pu.kind == "multi_ball":
            nb = Ball(ball.x, ball.y, -ball.vx,
                      ball.vy * random.uniform(0.6, 1.4))
            self.balls.append(nb)

        self.particles.emit_burst(pu.x, pu.y, pu.color, 60)

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self) -> None:
        if self.state == STATE_SPLASH:
            self.ui.draw_splash(16)
            return
        if self.state == STATE_MENU:
            self.ui.draw_menu(self.menu_sel)
            return
        if self.state == STATE_MODE:
            self.ui.draw_difficulty(self.diff_sel)
            return
        if self.state == STATE_WIN:
            self.ui.draw_win(self.winner, self.score, self.hits)
            return

        # Game world (playing / paused)
        offset = (0, 0)
        if self.shake > 0:
            offset = (random.randint(-6, 6), random.randint(-6, 6))
        self.screen.blit(self._bg, offset)

        self.pu_mgr.draw(self.screen)
        self.particles.draw(self.screen)

        for pad in self.paddles:
            pad.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)

        p2_name = "AI" if self.mode == "1p" else "P2"
        self.ui.draw_hud(self.score, "P1", p2_name, self.mode)

        if self.hint_timer > 0:
            self.ui.draw_controls_hint(self.mode)

        if self.state == STATE_PAUSED:
            self.ui.draw_pause()

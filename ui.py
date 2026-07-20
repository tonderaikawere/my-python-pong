# ui.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import pygame
import math
from constants import *


# ── Font helper ───────────────────────────────────────────────────────────────
def _font(size: int, bold: bool = False) -> pygame.font.Font:
    for name in ("Orbitron", "Rajdhani", "Exo 2", "Segoe UI", "Arial"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)


class UIManager:
    """Renders all non-gameplay screens and HUD elements."""

    def __init__(self, screen: pygame.Surface):
        self.screen    = screen
        self.W, self.H = screen.get_size()
        self.t         = 0.0

        # Fonts
        self.f_huge = _font(88, True)
        self.f_big  = _font(50, True)
        self.f_med  = _font(30, True)
        self.f_sm   = _font(20)
        self.f_xs   = _font(15)

        # Score flash
        self._flash     = [0, 0]   # remaining ms per player
        self._flash_dur = 650

        # Splash
        self._splash_t  = 0.0

    # ── Tick ──────────────────────────────────────────────────────────────────
    def update(self, dt: int) -> None:
        self.t        += dt * 0.001
        self._flash[0] = max(0, self._flash[0] - dt)
        self._flash[1] = max(0, self._flash[1] - dt)

    def flash_score(self, player: int) -> None:
        self._flash[player] = self._flash_dur

    # ── Splash ────────────────────────────────────────────────────────────────
    def draw_splash(self, dt: int) -> bool:
        """Returns True when splash is ready to dismiss."""
        self._splash_t += dt
        frac = min(1.0, self._splash_t / 2200)

        self.screen.fill(BG_COLOR)
        self._grid()

        alpha = int(255 * frac)
        cx    = self.W // 2

        # KawerifyTech logo text
        dev   = self.f_big.render("KawerifyTech", True, NEON_CYAN)
        pre   = self.f_med.render("presents", True, DIM_WHITE)
        game  = self.f_huge.render("My Python Pong", True, NEON_GREEN)
        url   = self.f_sm.render("kawerifytech.com", True, NEON_CYAN)
        ver   = self.f_xs.render(f"v{VERSION}", True, GRID_COLOR)

        self._blit_c_alpha(dev,  cx, self.H // 2 - 130, alpha)
        self._blit_c_alpha(pre,  cx, self.H // 2 -  62, alpha)
        self._blit_c_alpha(game, cx, self.H // 2 +  22, alpha)
        self._blit_c_alpha(url,  cx, self.H // 2 + 112, alpha)
        self._blit_c_alpha(ver,  cx, self.H // 2 + 138, alpha)

        # Animated separator line
        if frac > 0.6:
            w   = int((frac - 0.6) / 0.4 * 500)
            clr = (*NEON_CYAN, 180)
            s   = pygame.Surface((w, 2), pygame.SRCALPHA)
            s.fill(clr)
            self.screen.blit(s, (cx - w // 2, self.H // 2 - 10))

        # "Press any key" blink
        if self._splash_t > 1800:
            a2   = int(210 * abs(math.sin(self.t * 2)))
            hint = self.f_sm.render("Press any key to start", True, WHITE)
            self._blit_c_alpha(hint, cx, self.H - 55, a2)

        return self._splash_t > 1800

    # ── Main Menu ─────────────────────────────────────────────────────────────
    def draw_menu(self, selected: int) -> None:
        self.screen.fill(BG_COLOR)
        self._grid()
        self._title_banner()

        options = ["Single Player", "Two Players", "Quit"]
        cx      = self.W // 2

        for i, opt in enumerate(options):
            y   = self.H // 2 + 10 + i * 72
            col = NEON_CYAN if i == selected else DIM_WHITE
            if i == selected:
                # highlight box
                box = pygame.Rect(cx - 200, y - 26, 400, 52)
                pygame.draw.rect(self.screen, (*NEON_CYAN, 18), box, border_radius=10)
                pygame.draw.rect(self.screen, col, box, 2, border_radius=10)
                # arrow
                arr = self.f_med.render("▶", True, NEON_GREEN)
                ax  = box.left + 12 + math.sin(self.t * 4) * 4
                self.screen.blit(arr, (int(ax), y - arr.get_height() // 2))
            lbl = self.f_med.render(opt, True, col)
            self.screen.blit(lbl, (cx - lbl.get_width() // 2, y - lbl.get_height() // 2))

        nav = self.f_xs.render("↑ ↓  Navigate     Enter  Select", True, GRID_COLOR)
        self.screen.blit(nav, (cx - nav.get_width() // 2, self.H - 38))
        self._footer()

    # ── Difficulty ────────────────────────────────────────────────────────────
    def draw_difficulty(self, selected: int) -> None:
        self.screen.fill(BG_COLOR)
        self._grid()

        cx    = self.W // 2
        title = self.f_big.render("Select Difficulty", True, NEON_CYAN)
        self.screen.blit(title, (cx - title.get_width() // 2, 150))

        options = ["Easy",   "Medium", "Hard"]
        colors  = [NEON_GREEN, NEON_YELLOW, NEON_PINK]
        descs   = [
            "Relaxed — great for beginners",
            "Balanced — a fair challenge",
            "Brutal   — AI reads the future 😈",
        ]

        for i, (opt, col, dsc) in enumerate(zip(options, colors, descs)):
            y = self.H // 2 - 30 + i * 108
            c = col if i == selected else DIM_WHITE
            if i == selected:
                box = pygame.Rect(cx - 240, y - 34, 480, 74)
                pygame.draw.rect(self.screen, (*col, 22), box, border_radius=12)
                pygame.draw.rect(self.screen, col, box, 2, border_radius=12)
            lbl = self.f_med.render(opt, True, c)
            self.screen.blit(lbl, (cx - lbl.get_width() // 2, y - lbl.get_height() // 2))
            d = self.f_xs.render(dsc, True, DIM_WHITE if i == selected else GRID_COLOR)
            self.screen.blit(d,   (cx - d.get_width()   // 2, y + 24))

        esc = self.f_xs.render("Esc — Back     Enter — Start", True, GRID_COLOR)
        self.screen.blit(esc, (cx - esc.get_width() // 2, self.H - 38))
        self._footer()

    # ── HUD ───────────────────────────────────────────────────────────────────
    def draw_hud(self, score: list, p1: str, p2: str, mode: str) -> None:
        cx = self.W // 2

        # Centre dashes
        for y in range(20, self.H, 42):
            pygame.draw.rect(self.screen, MID_COLOR, (cx - 2, y, 4, 22), border_radius=2)

        # First-to label
        ft = self.f_xs.render(f"First to {WIN_SCORE}", True, GRID_COLOR)
        self.screen.blit(ft, (cx - ft.get_width() // 2, 6))

        # Score digits
        for idx, (sc, name, col, xp) in enumerate(zip(
            score,
            [p1, p2],
            [P1_COLOR, P2_COLOR],
            [cx - 130, cx + 80],
        )):
            frac  = self._flash[idx] / self._flash_dur if self._flash_dur else 0
            scale = 1.0 + frac * 0.38
            sc_s  = self.f_huge.render(str(sc), True, col)
            if scale > 1.01:
                sc_s = pygame.transform.smoothscale(
                    sc_s, (int(sc_s.get_width() * scale), int(sc_s.get_height() * scale))
                )
            self.screen.blit(sc_s, (xp - sc_s.get_width() // 2, 16))
            nm = self.f_xs.render(name, True, col)
            self.screen.blit(nm,  (xp - nm.get_width()  // 2, 108))

    # ── Pause ─────────────────────────────────────────────────────────────────
    def draw_pause(self) -> None:
        overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 148))
        self.screen.blit(overlay, (0, 0))

        cx, cy = self.W // 2, self.H // 2
        t = self.f_big.render("PAUSED", True, NEON_CYAN)
        self.screen.blit(t, (cx - t.get_width() // 2, cy - 90))

        hints = ["P  —  Resume", "R  —  Restart", "M  —  Main Menu", "S  —  Toggle Sound"]
        for i, h in enumerate(hints):
            s = self.f_sm.render(h, True, DIM_WHITE)
            self.screen.blit(s, (cx - s.get_width() // 2, cy - 10 + i * 44))

    # ── Win ───────────────────────────────────────────────────────────────────
    def draw_win(self, winner: str, score: list, hits: list) -> None:
        self.screen.fill(BG_COLOR)
        self._grid()

        cx, cy = self.W // 2, self.H // 2
        col    = P1_COLOR if "1" in winner else P2_COLOR

        # Pulsing winner text
        scl  = 1.0 + math.sin(self.t * 3) * 0.04
        wlbl = self.f_huge.render(f"{winner} Wins!", True, col)
        wlbl = pygame.transform.smoothscale(
            wlbl, (int(wlbl.get_width() * scl), int(wlbl.get_height() * scl))
        )
        self.screen.blit(wlbl, (cx - wlbl.get_width() // 2, cy - 190))

        # Score line
        sc_s = self.f_big.render(f"{score[0]}  —  {score[1]}", True, WHITE)
        self.screen.blit(sc_s, (cx - sc_s.get_width() // 2, cy - 75))

        # Stats
        stats = [f"P1 hits: {hits[0]}", f"P2 hits: {hits[1]}"]
        for i, st in enumerate(stats):
            s = self.f_sm.render(st, True, DIM_WHITE)
            self.screen.blit(s, (cx - s.get_width() // 2, cy + 10 + i * 40))

        # Buttons
        btns = [("Play Again", NEON_GREEN), ("Main Menu", NEON_CYAN)]
        for i, (lbl, c) in enumerate(btns):
            y   = cy + 120 + i * 64
            box = pygame.Rect(cx - 170, y - 24, 340, 48)
            pygame.draw.rect(self.screen, (*c, 35), box, border_radius=11)
            pygame.draw.rect(self.screen, c,       box, 2,  border_radius=11)
            s = self.f_med.render(lbl, True, c)
            self.screen.blit(s, (cx - s.get_width() // 2, y - s.get_height() // 2))

        hint = self.f_xs.render("Enter — Play Again     M — Main Menu", True, GRID_COLOR)
        self.screen.blit(hint, (cx - hint.get_width() // 2, self.H - 38))
        self._footer()

    # ── Controls hint ─────────────────────────────────────────────────────────
    def draw_controls_hint(self, mode: str) -> None:
        parts = ["W / S — Player 1"]
        if mode == "2p":
            parts.append("↑ / ↓ — Player 2")
        parts.append("P — Pause")
        text = "   |   ".join(parts)
        s    = self.f_xs.render(text, True, GRID_COLOR)
        self.screen.blit(s, (self.W // 2 - s.get_width() // 2, self.H - 28))

    # ── Internal helpers ──────────────────────────────────────────────────────
    def _grid(self) -> None:
        for x in range(0, self.W, 80):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, self.H))
        for y in range(0, self.H, 80):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (self.W, y))

    def _title_banner(self) -> None:
        cx    = self.W // 2
        title = self.f_big.render("My Python Pong", True, NEON_CYAN)
        sub   = self.f_sm.render("by KawerifyTech", True, NEON_GREEN)
        self.screen.blit(title, (cx - title.get_width() // 2, 80))
        self.screen.blit(sub,   (cx - sub.get_width()   // 2, 144))

    def _footer(self) -> None:
        f = self.f_xs.render("© 2024 KawerifyTech · kawerifytech.com", True, GRID_COLOR)
        self.screen.blit(f, (self.W // 2 - f.get_width() // 2, self.H - 18))

    def _blit_c_alpha(self, surf: pygame.Surface, cx: int, y: int, alpha: int) -> None:
        tmp = surf.copy()
        tmp.set_alpha(alpha)
        self.screen.blit(tmp, (cx - surf.get_width() // 2, y - surf.get_height() // 2))

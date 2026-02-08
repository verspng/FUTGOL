"""Team management and roster."""
from __future__ import annotations

import pygame

from futgol import settings
from futgol.player import Player


class Team:
    """Represents a football team."""

    def __init__(self, name: str, side: str) -> None:
        self.name = name
        self.side = side
        self.players: list[Player] = []
        self._build_team()

    def _build_team(self) -> None:
        pitch_left = settings.PITCH_MARGIN
        pitch_right = settings.PITCH_MARGIN + settings.PITCH_WIDTH
        pitch_top = settings.PITCH_MARGIN
        pitch_bottom = settings.PITCH_MARGIN + settings.PITCH_HEIGHT
        x_offset = pitch_left + settings.PITCH_WIDTH * (0.25 if self.side == "home" else 0.75)

        rows = [pitch_top + settings.PITCH_HEIGHT * ratio for ratio in (0.18, 0.36, 0.54, 0.72)]
        for idx in range(10):
            row = rows[idx % len(rows)]
            col_offset = (idx // len(rows)) * 30
            position = pygame.Vector2(x_offset + col_offset, row)
            self.players.append(Player(f"{self.name}-{idx+1}", self.side, position))

        keeper_x = pitch_left + 30 if self.side == "home" else pitch_right - 30
        keeper_position = pygame.Vector2(keeper_x, pitch_top + settings.PITCH_HEIGHT / 2)
        self.players.append(Player(f"{self.name}-GK", self.side, keeper_position, is_goalkeeper=True))

    def get_closest_to_ball(self, ball_position: pygame.Vector2) -> Player:
        return min(self.players, key=lambda player: player.position.distance_squared_to(ball_position))

    def reset_positions(self) -> None:
        for player in self.players:
            player.position = pygame.Vector2(player.home_position)
            player.velocity.update(0, 0)
            player.has_ball = False
            player.selected = False

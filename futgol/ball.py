"""Ball physics and rendering."""
from __future__ import annotations

import pygame

from futgol import settings


class Ball:
    """Simple physics model for the ball."""

    def __init__(self, position: pygame.Vector2) -> None:
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        self.owner = None

    def update(self, dt: float, pitch_rect: pygame.Rect) -> None:
        if self.owner:
            self.position = self.owner.position + pygame.Vector2(0, -settings.PLAYER_RADIUS // 2)
            self.velocity.update(0, 0)
            return
        self.position += self.velocity * dt
        self.velocity *= 0.98

        if self.position.x - settings.BALL_RADIUS <= pitch_rect.left or self.position.x + settings.BALL_RADIUS >= pitch_rect.right:
            self.velocity.x *= -0.8
            self.position.x = max(pitch_rect.left + settings.BALL_RADIUS, min(self.position.x, pitch_rect.right - settings.BALL_RADIUS))
        if self.position.y - settings.BALL_RADIUS <= pitch_rect.top or self.position.y + settings.BALL_RADIUS >= pitch_rect.bottom:
            self.velocity.y *= -0.8
            self.position.y = max(pitch_rect.top + settings.BALL_RADIUS, min(self.position.y, pitch_rect.bottom - settings.BALL_RADIUS))

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, settings.COLOR_BALL, (int(self.position.x), int(self.position.y)), settings.BALL_RADIUS)
        pygame.draw.circle(surface, (10, 10, 10), (int(self.position.x), int(self.position.y)), settings.BALL_RADIUS, 1)

    def kick(self, direction: pygame.Vector2, power: float) -> None:
        self.owner = None
        if direction.length_squared() == 0:
            return
        self.velocity = direction.normalize() * power

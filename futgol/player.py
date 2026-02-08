"""Player entity and animation state."""
from __future__ import annotations

from dataclasses import dataclass

import pygame

from futgol import settings


@dataclass
class Animation:
    frames: list[tuple[int, int, int]]
    frame_time: float


class Player:
    """Represents a football player."""

    def __init__(self, name: str, team: str, position: pygame.Vector2, is_goalkeeper: bool = False) -> None:
        self.name = name
        self.team = team
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.home_position = pygame.Vector2(position)
        self.is_goalkeeper = is_goalkeeper
        self.has_ball = False
        self.selected = False
        self.skill_cooldowns: dict[str, float] = {}
        self.animation_state = "idle"
        self.animation_timer = 0.0
        self.current_frame = 0
        self.animations = {
            "idle": Animation([(255, 255, 255)], 0.5),
            "run": Animation([(255, 255, 255), (220, 220, 220)], 0.12),
            "kick": Animation([(255, 220, 220), (255, 180, 180)], 0.08),
            "skill": Animation([(255, 255, 180), (255, 240, 120)], 0.1),
        }

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self._update_animation(dt)

    def _update_animation(self, dt: float) -> None:
        if self.velocity.length_squared() > 1:
            self.animation_state = "run"
        else:
            self.animation_state = "idle"
        animation = self.animations[self.animation_state]
        self.animation_timer += dt
        if self.animation_timer >= animation.frame_time:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % len(animation.frames)

    def render(self, surface: pygame.Surface) -> None:
        base_color = settings.COLOR_HOME if self.team == "home" else settings.COLOR_AWAY
        animation = self.animations[self.animation_state]
        tint = animation.frames[self.current_frame]
        color = (
            min(255, base_color[0] + tint[0] // 6),
            min(255, base_color[1] + tint[1] // 6),
            min(255, base_color[2] + tint[2] // 6),
        )
        shadow_pos = (int(self.position.x), int(self.position.y) + settings.PLAYER_RADIUS + 4)
        pygame.draw.circle(surface, settings.COLOR_SHADOW, shadow_pos, settings.PLAYER_RADIUS + 2)
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), settings.PLAYER_RADIUS)
        if self.selected:
            pygame.draw.circle(
                surface,
                settings.COLOR_SELECTED,
                (int(self.position.x), int(self.position.y)),
                settings.PLAYER_RADIUS + 4,
                2,
            )

    def clamp_to_pitch(self, pitch_rect: pygame.Rect) -> None:
        self.position.x = max(pitch_rect.left + settings.PLAYER_RADIUS, min(self.position.x, pitch_rect.right - settings.PLAYER_RADIUS))
        self.position.y = max(pitch_rect.top + settings.PLAYER_RADIUS, min(self.position.y, pitch_rect.bottom - settings.PLAYER_RADIUS))

    def ready_for_skill(self, skill: str, current_time: float) -> bool:
        return self.skill_cooldowns.get(skill, 0.0) <= current_time

    def set_skill_cooldown(self, skill: str, current_time: float) -> None:
        self.skill_cooldowns[skill] = current_time + settings.SKILL_COOLDOWN

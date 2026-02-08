"""Match orchestration and rules."""
from __future__ import annotations

import pygame

from futgol import settings
from futgol.ai_system import AISystem
from futgol.ball import Ball
from futgol.player import Player
from futgol.team import Team


class Match:
    """Core match logic."""

    def __init__(self) -> None:
        self.pitch_rect = pygame.Rect(settings.PITCH_RECT)
        self.ball = Ball(pygame.Vector2(self.pitch_rect.center))
        self.home_team = Team("Home", "home")
        self.away_team = Team("Away", "away")
        self.ai = AISystem()
        self.controlled_player = self.home_team.players[0]
        self.controlled_player.selected = True
        self.score = {"home": 0, "away": 0}
        self.last_touch: Player | None = None

    def update(self, dt: float, input_manager, current_time: float) -> None:
        self._handle_player_selection()
        self._handle_controlled_input(dt, input_manager, current_time)
        self.ai.update_players(self.away_team.players, self.ball.position, self.ball.owner)
        self.ai.update_players(self.home_team.players, self.ball.position, self.ball.owner)

        for player in self.home_team.players + self.away_team.players:
            player.update(dt)
            player.clamp_to_pitch(self.pitch_rect)

        self._resolve_ball_possession()
        self.ball.update(dt, self.pitch_rect)
        self._check_goal()

    def _handle_controlled_input(self, dt: float, input_manager, current_time: float) -> None:
        direction = input_manager.movement
        if direction.length_squared() > 0:
            self.controlled_player.velocity = direction * settings.PLAYER_SPEED
        else:
            self.controlled_player.velocity.update(0, 0)

        if input_manager.shoot:
            self._shoot()
        if input_manager.pass_ball:
            self._pass_ball()
        if input_manager.skill:
            self._use_skill(input_manager.skill, current_time)

    def _resolve_ball_possession(self) -> None:
        if self.ball.owner:
            return
        for player in self.home_team.players + self.away_team.players:
            if player.position.distance_to(self.ball.position) < settings.PLAYER_RADIUS + settings.BALL_RADIUS + 2:
                self.ball.owner = player
                player.has_ball = True
                self.last_touch = player
                if player.team == "home":
                    self._set_controlled(player)
                break

    def _shoot(self) -> None:
        if not self.ball.owner:
            return
        direction = pygame.Vector2(1 if self.ball.owner.team == "home" else -1, 0)
        self.ball.kick(direction, settings.SHOT_POWER)
        self.ball.owner.has_ball = False
        self.ball.owner = None

    def _pass_ball(self) -> None:
        if not self.ball.owner:
            return
        teammates = [p for p in (self.home_team.players if self.ball.owner.team == "home" else self.away_team.players) if p is not self.ball.owner]
        target = min(teammates, key=lambda player: player.position.distance_squared_to(self.ball.owner.position))
        direction = target.position - self.ball.owner.position
        self.ball.kick(direction, settings.PASS_POWER)
        self.ball.owner.has_ball = False
        self.ball.owner = None
        if target.team == "home":
            self._set_controlled(target)

    def _use_skill(self, skill: str, current_time: float) -> None:
        if not self.ball.owner or self.ball.owner.team != "home":
            return
        player = self.ball.owner
        if not player.ready_for_skill(skill, current_time):
            return
        player.set_skill_cooldown(skill, current_time)
        direction = pygame.Vector2(1, -0.2)
        if skill in {"header", "bicycle"}:
            power = settings.HEADER_POWER
        else:
            power = settings.PASS_POWER * 1.15
        self.ball.kick(direction, power)
        self.ball.owner.has_ball = False
        self.ball.owner = None

    def _handle_player_selection(self) -> None:
        if self.ball.owner and self.ball.owner.team == "home":
            self._set_controlled(self.ball.owner)
        elif not self.ball.owner:
            closest = self.home_team.get_closest_to_ball(self.ball.position)
            self._set_controlled(closest)

    def _set_controlled(self, player: Player) -> None:
        if self.controlled_player is player:
            return
        self.controlled_player.selected = False
        self.controlled_player = player
        self.controlled_player.selected = True

    def _check_goal(self) -> None:
        goal_left = pygame.Rect(
            self.pitch_rect.left - settings.GOAL_DEPTH,
            self.pitch_rect.centery - settings.GOAL_WIDTH / 2,
            settings.GOAL_DEPTH,
            settings.GOAL_WIDTH,
        )
        goal_right = pygame.Rect(
            self.pitch_rect.right,
            self.pitch_rect.centery - settings.GOAL_WIDTH / 2,
            settings.GOAL_DEPTH,
            settings.GOAL_WIDTH,
        )
        if goal_left.collidepoint(self.ball.position):
            self.score["away"] += 1
            self._reset_after_goal()
        if goal_right.collidepoint(self.ball.position):
            self.score["home"] += 1
            self._reset_after_goal()

    def _reset_after_goal(self) -> None:
        self.home_team.reset_positions()
        self.away_team.reset_positions()
        self.ball.position = pygame.Vector2(self.pitch_rect.center)
        self.ball.velocity.update(0, 0)
        self.ball.owner = None
        self._set_controlled(self.home_team.players[0])

    def render(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        self._draw_pitch(surface)
        for player in self.home_team.players + self.away_team.players:
            player.render(surface)
        self.ball.render(surface)
        score_text = font.render(f"{self.score['home']} - {self.score['away']}", True, settings.COLOR_LINES)
        surface.blit(score_text, (settings.SCREEN_WIDTH / 2 - score_text.get_width() / 2, 20))

    def _draw_pitch(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BG)
        pygame.draw.rect(surface, settings.COLOR_PITCH, self.pitch_rect)
        pygame.draw.rect(surface, settings.COLOR_LINES, self.pitch_rect, 4)
        center = self.pitch_rect.center
        pygame.draw.line(surface, settings.COLOR_LINES, (center[0], self.pitch_rect.top), (center[0], self.pitch_rect.bottom), 2)
        pygame.draw.circle(surface, settings.COLOR_LINES, center, 80, 2)
        pygame.draw.rect(
            surface,
            settings.COLOR_LINES,
            (
                self.pitch_rect.left,
                self.pitch_rect.centery - settings.GOAL_WIDTH / 2,
                settings.GOAL_DEPTH,
                settings.GOAL_WIDTH,
            ),
            2,
        )
        pygame.draw.rect(
            surface,
            settings.COLOR_LINES,
            (
                self.pitch_rect.right - settings.GOAL_DEPTH,
                self.pitch_rect.centery - settings.GOAL_WIDTH / 2,
                settings.GOAL_DEPTH,
                settings.GOAL_WIDTH,
            ),
            2,
        )

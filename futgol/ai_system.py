"""AI behaviors for non-controlled players."""
from __future__ import annotations

import pygame

from futgol import settings
from futgol.player import Player


class AISystem:
    """Very lightweight AI for positioning and ball chasing."""

    def update_players(self, players: list[Player], ball_position: pygame.Vector2, ball_owner: Player | None) -> None:
        for player in players:
            if player.selected:
                continue
            if player.is_goalkeeper:
                self._update_goalkeeper(player, ball_position)
            else:
                self._update_field_player(player, ball_position, ball_owner)

    def _update_field_player(self, player: Player, ball_position: pygame.Vector2, ball_owner: Player | None) -> None:
        target = pygame.Vector2(player.home_position)
        distance_to_ball = player.position.distance_to(ball_position)
        if ball_owner and ball_owner.team != player.team and distance_to_ball < 160:
            target = ball_position
        elif not ball_owner and distance_to_ball < 140:
            target = ball_position

        direction = target - player.position
        if direction.length_squared() > 1:
            player.velocity = direction.normalize() * settings.PLAYER_SPEED * 0.6
        else:
            player.velocity.update(0, 0)

    def _update_goalkeeper(self, player: Player, ball_position: pygame.Vector2) -> None:
        target = pygame.Vector2(player.home_position)
        if abs(ball_position.x - player.home_position.x) < 220:
            target.y = ball_position.y
        direction = target - player.position
        if direction.length_squared() > 1:
            player.velocity = direction.normalize() * settings.PLAYER_SPEED * 0.55
        else:
            player.velocity.update(0, 0)

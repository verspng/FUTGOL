"""Handles input mapping and action triggers."""
from __future__ import annotations

import pygame


class InputManager:
    """Maps keyboard/mouse input to game actions."""

    def __init__(self) -> None:
        self.movement = pygame.Vector2(0, 0)
        self.shoot = False
        self.pass_ball = False
        self.skill = None
        self.pause = False

    def process(self, events: list[pygame.event.Event]) -> None:
        self.shoot = False
        self.pass_ball = False
        self.skill = None
        self.pause = False

        keys = pygame.key.get_pressed()
        self.movement = pygame.Vector2(
            (1 if keys[pygame.K_d] else 0) - (1 if keys[pygame.K_a] else 0),
            (1 if keys[pygame.K_s] else 0) - (1 if keys[pygame.K_w] else 0),
        )
        if self.movement.length_squared() > 1:
            self.movement = self.movement.normalize()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = True
                if event.key == pygame.K_q:
                    self.skill = "header"
                if event.key == pygame.K_c:
                    self.skill = "bicycle"
                if event.key == pygame.K_f:
                    self.skill = "skill_f"
                if event.key == pygame.K_x:
                    self.skill = "fake_shoot"
                if event.key == pygame.K_z:
                    self.skill = "croqueta"
                if event.key == pygame.K_v:
                    self.skill = "rainbow"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shoot = True
                if event.button == 3:
                    self.pass_ball = True

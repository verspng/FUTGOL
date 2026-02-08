"""Menu handling for main and pause screens."""
from __future__ import annotations

import pygame

from futgol import settings


class MenuSystem:
    """Simple menu system with selectable options."""

    def __init__(self) -> None:
        self.main_options = ["Jugar Partido", "Opciones", "Salir"]
        self.pause_options = ["Reanudar", "Opciones", "Salir"]
        self.team_options = ["Home", "Away"]
        self.main_index = 0
        self.pause_index = 0
        self.team_index = 0
        self.state = "main"

    def handle_input(self, events: list[pygame.event.Event]) -> str | None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_UP, pygame.K_w}:
                    self._move(-1)
                if event.key in {pygame.K_DOWN, pygame.K_s}:
                    self._move(1)
                if event.key == pygame.K_RETURN:
                    return self._select()
        return None

    def _move(self, direction: int) -> None:
        if self.state == "main":
            self.main_index = (self.main_index + direction) % len(self.main_options)
        elif self.state == "pause":
            self.pause_index = (self.pause_index + direction) % len(self.pause_options)
        elif self.state == "team":
            self.team_index = (self.team_index + direction) % len(self.team_options)

    def _select(self) -> str | None:
        if self.state == "main":
            choice = self.main_options[self.main_index]
            if choice == "Jugar Partido":
                self.state = "team"
                return "team"
            if choice == "Salir":
                return "quit"
        elif self.state == "pause":
            choice = self.pause_options[self.pause_index]
            if choice == "Reanudar":
                return "resume"
            if choice == "Salir":
                return "quit"
        elif self.state == "team":
            return "start_match"
        return None

    def render(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        surface.fill(settings.COLOR_BG)
        if self.state == "main":
            self._draw_menu(surface, font, "FUTGOL", self.main_options, self.main_index)
        elif self.state == "pause":
            self._draw_menu(surface, font, "PAUSA", self.pause_options, self.pause_index)
        elif self.state == "team":
            self._draw_menu(surface, font, "Selecciona Equipo", self.team_options, self.team_index)

    def _draw_menu(self, surface: pygame.Surface, font: pygame.font.Font, title: str, options: list[str], index: int) -> None:
        title_surface = font.render(title, True, settings.COLOR_LINES)
        surface.blit(title_surface, (settings.SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 140))
        for idx, option in enumerate(options):
            color = settings.COLOR_SELECTED if idx == index else settings.COLOR_LINES
            option_surface = font.render(option, True, color)
            surface.blit(option_surface, (settings.SCREEN_WIDTH / 2 - option_surface.get_width() / 2, 240 + idx * 60))

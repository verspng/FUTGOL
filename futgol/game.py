"""Main game application."""
from __future__ import annotations

import sys

import pygame

from futgol import settings
from futgol.input_manager import InputManager
from futgol.match import Match
from futgol.menu_system import MenuSystem


class Game:
    """Game state and loop."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("FUTGOL")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(settings.FONT_NAME, 32)
        self.menu = MenuSystem()
        self.match = Match()
        self.input_manager = InputManager()
        self.state = "menu"

    def run(self) -> None:
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0
            current_time = pygame.time.get_ticks() / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self._quit()

            if self.state == "menu":
                action = self.menu.handle_input(events)
                if action == "start_match":
                    self.state = "match"
                    self.menu.state = "pause"
                if action == "quit":
                    self._quit()
                self.menu.render(self.screen, self.font)
            elif self.state == "pause":
                action = self.menu.handle_input(events)
                if action == "resume":
                    self.state = "match"
                if action == "quit":
                    self._quit()
                self.menu.render(self.screen, self.font)
            elif self.state == "match":
                self.input_manager.process(events)
                if self.input_manager.pause:
                    self.state = "pause"
                self.match.update(dt, self.input_manager, current_time)
                self.match.render(self.screen, self.font)

            pygame.display.flip()

    def _quit(self) -> None:
        pygame.quit()
        sys.exit()

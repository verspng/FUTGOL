"""Entry point for FUTGOL."""
from __future__ import annotations

from futgol.game import Game


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

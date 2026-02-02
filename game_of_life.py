"""
Conway's Game of Life - A cellular automaton simulation.

Rules:
1. Any live cell with 2 or 3 live neighbors survives.
2. Any dead cell with exactly 3 live neighbors becomes a live cell.
3. All other live cells die, and all other dead cells stay dead.
"""

import os
import time
import random
import argparse
from typing import Set, Tuple

# Type alias for cell coordinates
Cell = Tuple[int, int]


class GameOfLife:
    """Conway's Game of Life simulation."""

    def __init__(self, width: int = 40, height: int = 20):
        """Initialize the game with given dimensions."""
        self.width = width
        self.height = height
        self.alive_cells: Set[Cell] = set()

    def randomize(self, density: float = 0.3) -> None:
        """Populate the grid with random live cells."""
        self.alive_cells.clear()
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    self.alive_cells.add((x, y))

    def set_pattern(self, pattern: str) -> None:
        """Set a predefined pattern on the grid."""
        self.alive_cells.clear()
        center_x, center_y = self.width // 2, self.height // 2

        patterns = {
            "glider": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
            "blinker": [(0, 0), (1, 0), (2, 0)],
            "beacon": [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)],
            "toad": [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],
            "pulsar": [
                # Top section
                (-2, -4), (-3, -4), (-4, -4), (2, -4), (3, -4), (4, -4),
                (-4, -2), (-4, -3), (4, -2), (4, -3),
                (-2, -1), (-3, -1), (-4, -1), (2, -1), (3, -1), (4, -1),
                # Bottom section (mirrored)
                (-2, 4), (-3, 4), (-4, 4), (2, 4), (3, 4), (4, 4),
                (-4, 2), (-4, 3), (4, 2), (4, 3),
                (-2, 1), (-3, 1), (-4, 1), (2, 1), (3, 1), (4, 1),
            ],
            "glider_gun": [
                # Left square
                (0, 4), (0, 5), (1, 4), (1, 5),
                # Left part
                (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (12, 2), (12, 8),
                (13, 2), (13, 8), (14, 5), (15, 3), (15, 7), (16, 4), (16, 5),
                (16, 6), (17, 5),
                # Right part
                (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4),
                (22, 1), (22, 5), (24, 0), (24, 1), (24, 5), (24, 6),
                # Right square
                (34, 2), (34, 3), (35, 2), (35, 3),
            ],
        }

        if pattern in patterns:
            for dx, dy in patterns[pattern]:
                x, y = center_x + dx, center_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.alive_cells.add((x, y))
        else:
            print(f"Unknown pattern: {pattern}. Using random.")
            self.randomize()

    def get_neighbors(self, cell: Cell) -> Set[Cell]:
        """Get all 8 neighbors of a cell."""
        x, y = cell
        neighbors = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                # Wrap around edges (toroidal grid)
                nx = nx % self.width
                ny = ny % self.height
                neighbors.add((nx, ny))
        return neighbors

    def count_alive_neighbors(self, cell: Cell) -> int:
        """Count how many neighbors of a cell are alive."""
        return len(self.get_neighbors(cell) & self.alive_cells)

    def step(self) -> None:
        """Advance the simulation by one generation."""
        new_alive = set()

        # Check all cells that might change state
        cells_to_check = set(self.alive_cells)
        for cell in self.alive_cells:
            cells_to_check |= self.get_neighbors(cell)

        for cell in cells_to_check:
            alive_neighbors = self.count_alive_neighbors(cell)
            if cell in self.alive_cells:
                # Cell is alive: survives with 2 or 3 neighbors
                if alive_neighbors in (2, 3):
                    new_alive.add(cell)
            else:
                # Cell is dead: becomes alive with exactly 3 neighbors
                if alive_neighbors == 3:
                    new_alive.add(cell)

        self.alive_cells = new_alive

    def render(self) -> str:
        """Render the current state as a string."""
        lines = []
        lines.append("+" + "-" * self.width + "+")
        for y in range(self.height):
            row = "|"
            for x in range(self.width):
                if (x, y) in self.alive_cells:
                    row += "█"
                else:
                    row += " "
            row += "|"
            lines.append(row)
        lines.append("+" + "-" * self.width + "+")
        return "\n".join(lines)

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def run(self, generations: int = 100, delay: float = 0.1) -> None:
        """Run the simulation for a number of generations."""
        for gen in range(generations):
            self.clear_screen()
            print(f"Conway's Game of Life - Generation {gen + 1}/{generations}")
            print(f"Alive cells: {len(self.alive_cells)}")
            print(self.render())
            print("\nPress Ctrl+C to stop")

            if len(self.alive_cells) == 0:
                print("\nAll cells have died. Simulation ended.")
                break

            time.sleep(delay)
            self.step()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "-w", "--width", type=int, default=40, help="Grid width (default: 40)"
    )
    parser.add_argument(
        "-H", "--height", type=int, default=20, help="Grid height (default: 20)"
    )
    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        default=200,
        help="Number of generations (default: 200)",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0.1,
        help="Delay between generations in seconds (default: 0.1)",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        default="random",
        choices=["random", "glider", "blinker", "beacon", "toad", "pulsar", "glider_gun"],
        help="Starting pattern (default: random)",
    )
    parser.add_argument(
        "--density",
        type=float,
        default=0.3,
        help="Cell density for random pattern (default: 0.3)",
    )

    args = parser.parse_args()

    game = GameOfLife(width=args.width, height=args.height)

    if args.pattern == "random":
        game.randomize(density=args.density)
    else:
        game.set_pattern(args.pattern)

    try:
        game.run(generations=args.generations, delay=args.delay)
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user.")


if __name__ == "__main__":
    main()

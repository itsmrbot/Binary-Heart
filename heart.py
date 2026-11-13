#!/usr/bin/env python3
"""Binary Heart: a pulsing, animated ASCII heart for your terminal.

Run ``python heart.py --help`` to see all available options.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
import time
from typing import List, Optional, Sequence, Tuple

# ANSI escape codes
RED = "\033[91m"
PINK = "\033[95m"
RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"

HEART_CHARS = "0011010101001001"
SPARKLE_CHARS = "101"

# Cell kinds stored in the grid
EMPTY, HEART, SPARKLE = 0, 1, 2

Cell = Tuple[int, str]  # (kind, character)


def heart_x(t: float) -> float:
    """X coordinate of the parametric heart curve at angle ``t``."""
    return 16 * (math.sin(t) ** 3)


def heart_y(t: float) -> float:
    """Y coordinate of the parametric heart curve (inverted for terminals)."""
    return -(
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )


def build_frame(
    frame: int,
    width: int,
    height: int,
    sparkles: int = 15,
) -> List[List[Cell]]:
    """Return a grid of cells for the given animation frame."""
    grid: List[List[Cell]] = [[(EMPTY, " ")] * width for _ in range(height)]

    # Pulsing size effect
    scale = 1.0 + 0.12 * math.sin(frame * 0.35)

    # Draw the heart outline
    t = 0.0
    while t < 2 * math.pi:
        x = int(width / 2 + heart_x(t) * scale * 1.3)
        y = int(height / 2 + heart_y(t) * scale * 0.65)
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = (HEART, random.choice(HEART_CHARS))
        t += 0.02

    # Sprinkle some sparkles on empty cells
    for _ in range(sparkles):
        px = random.randrange(width)
        py = random.randrange(height)
        if grid[py][px][0] == EMPTY:
            grid[py][px] = (SPARKLE, random.choice(SPARKLE_CHARS))

    return grid


def render(grid: List[List[Cell]], use_color: bool) -> str:
    """Convert a grid of cells into a printable string."""
    lines = []
    for row in grid:
        parts = []
        for kind, char in row:
            if kind == EMPTY or not use_color:
                parts.append(char)
            elif kind == HEART:
                parts.append(f"{RED}{char}{RESET}")
            else:
                parts.append(f"{PINK}{char}{RESET}")
        lines.append("".join(parts))
    return "\n".join(lines)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Display a pulsing, animated ASCII heart in your terminal."
    )
    parser.add_argument(
        "-m", "--message",
        default="You mean the world to me!",
        help="message shown under the heart (default: %(default)s)",
    )
    parser.add_argument(
        "-f", "--frames", type=int, default=120,
        help="number of frames to play; 0 loops until Ctrl+C (default: %(default)s)",
    )
    parser.add_argument(
        "--fps", type=float, default=12.5,
        help="frames per second (default: %(default)s)",
    )
    parser.add_argument(
        "--width", type=int, default=70,
        help="canvas width in characters (default: %(default)s)",
    )
    parser.add_argument(
        "--height", type=int, default=30,
        help="canvas height in lines (default: %(default)s)",
    )
    parser.add_argument(
        "--no-color", action="store_true",
        help="disable ANSI colors",
    )
    args = parser.parse_args(argv)

    if args.fps <= 0:
        parser.error("--fps must be greater than 0")
    if args.width < 40 or args.height < 20:
        parser.error("--width must be at least 40 and --height at least 20")
    if args.frames < 0:
        parser.error("--frames cannot be negative")
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    use_color = not args.no_color and sys.stdout.isatty()

    # Enables ANSI escape sequence processing on Windows terminals.
    if os.name == "nt":
        os.system("")

    delay = 1.0 / args.fps
    caption = f"💌 {args.message} 💌".center(args.width)
    if use_color:
        caption = f"{PINK}{caption}{RESET}"

    try:
        if use_color:
            print(HIDE_CURSOR + CLEAR_SCREEN, end="")
        frame = 0
        while args.frames == 0 or frame < args.frames:
            grid = build_frame(frame, args.width, args.height)
            # Move the cursor home instead of clearing, to avoid flicker.
            print(CURSOR_HOME + render(grid, use_color) + "\n\n" + caption, flush=True)
            time.sleep(delay)
            frame += 1
    except KeyboardInterrupt:
        print("\nAnimation stopped.")
    finally:
        if use_color:
            print(SHOW_CURSOR, end="", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

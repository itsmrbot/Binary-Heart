# 💌 Binary Heart

A tiny, dependency-free Python script that draws a **pulsing heart made of 0s and 1s** right in your terminal. Great as a small gift, a Valentine's surprise, or a fun first project to learn about parametric curves and terminal animation.


## Features

- Pulsing heart drawn from a parametric equation
- Random binary digits (`0` / `1`) that flicker every frame
- Red heart outline with pink sparkles
- Customizable message, speed, size and length
- Flicker-free rendering, cursor is hidden while playing and restored on exit
- Works on Linux, macOS and Windows 10+
- Pure standard library, no `pip install` needed

## Requirements

- Python 3.8 or newer
- A terminal that supports ANSI colors (most modern terminals do)

## Quick start

```bash
git clone https://github.com/itsmrbot/Binary-Heart.git
cd Binary-Heart
python heart.py
```

## Usage

```bash
python heart.py 
```

| Option | Description | Default |
| --- | --- | --- |
| `-m`, `--message` | Text shown under the heart | `You mean the world to me!` |
| `-f`, `--frames` | Number of frames to play (`0` = loop until Ctrl+C) | `120` |
| `--fps` | Frames per second | `12.5` |
| `--width` | Canvas width in characters | `70` |
| `--height` | Canvas height in lines | `30` |
| `--no-color` | Disable ANSI colors | off |
| `-h`, `--help` | Show help and exit | |

### Examples

```bash
# Personal message
python heart.py -m "Thanks for being with me."

# Play forever until you press Ctrl+C
python heart.py --frames 0

# Slower, bigger animation
python heart.py --fps 8 --width 90 --height 40
```

## How it works

The heart shape comes from the classic parametric equations:

```
x(t) = 16 · sin³(t)
y(t) = 13·cos(t) − 5·cos(2t) − 2·cos(3t) − cos(4t)
```

For every frame, the script:

1. Samples `t` from `0` to `2π` and maps each point to a cell on a character grid.
2. Scales the heart with a sine wave to create the **pulse** effect.
3. Fills each outline cell with a random `0` or `1`.
4. Adds a few random sparkles, then prints the whole frame in one go.


## Troubleshooting

- **Weird characters like `←[91m` on Windows:** use Windows Terminal or Windows 10+ with a recent console, or run with `--no-color`.
- **Heart looks squished:** terminal characters are taller than wide; adjust `--width` and `--height` to suit your window.
- **Emoji not showing:** your terminal font may not support emoji; the animation still works.

## Contributing

Ideas, issues and pull requests are welcome. Some ideas:

- Extra shapes (star, rainbow, your initials)
- More color themes
- Custom character sets

## License

Released under the [MIT License](LICENSE).

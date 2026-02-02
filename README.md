# Conway's Game of Life

A terminal-based implementation of Conway's Game of Life cellular automaton.

## Rules

1. Any live cell with 2 or 3 live neighbors survives
2. Any dead cell with exactly 3 live neighbors becomes alive
3. All other cells die or stay dead

## Usage

```bash
python game_of_life.py [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-w, --width` | Grid width | 40 |
| `-H, --height` | Grid height | 20 |
| `-g, --generations` | Number of generations | 200 |
| `-d, --delay` | Delay between generations (seconds) | 0.1 |
| `-p, --pattern` | Starting pattern | random |
| `--density` | Cell density for random pattern | 0.3 |

### Patterns

- `random` - Random cell distribution
- `glider` - A moving glider
- `blinker` - Simple oscillator (period 2)
- `beacon` - Oscillator (period 2)
- `toad` - Oscillator (period 2)
- `pulsar` - Larger oscillator (period 3)
- `glider_gun` - Gosper glider gun (produces gliders)

## Examples

```bash
# Run with default settings (random pattern)
python game_of_life.py

# Run with a glider pattern
python game_of_life.py -p glider

# Run with custom grid size
python game_of_life.py -w 60 -H 30

# Run the glider gun on a larger grid
python game_of_life.py -p glider_gun -w 80 -H 40 -g 500
```

Press `Ctrl+C` to stop the simulation at any time.


# Tetris Game

A classic Tetris implementation built with Python and Pygame, featuring all standard gameplay mechanics and a clean, modular codebase.

## Features

- **Complete Tetris Experience**: All 7 standard tetromino pieces (I, O, T, S, Z, J, L)
- **Standard Gameplay**: Line clearing, scoring, level progression, and increasing difficulty
- **Visual Enhancements**: Ghost piece preview, next piece display, and clean graphics
- **Game States**: Pause functionality, game over detection, and restart capability
- **Modular Design**: Separated controls, game logic, and rendering for easy maintenance

## Requirements

- Python 3.6 or higher
- Pygame library

## Installation

1. Install Python from [python.org](https://python.org)
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Download or clone this repository
4. Run the game:
   ```bash
   python main.py
   ```

## Controls

| Key | Action |
|-----|--------|
| A / ← | Move left |
| D / → | Move right |
| S / ↓ | Soft drop (faster fall) |
| W / ↑ / Space | Rotate piece |
| Z | Hard drop (instant drop) |
| P | Pause/Unpause |
| ESC | Quit game |
| R | Restart (when game over) |

## Gameplay

- **Objective**: Clear horizontal lines by filling them completely with blocks
- **Scoring**: 
  - Single line: 100 × level
  - Double line: 300 × level
  - Triple line: 500 × level
  - Tetris (4 lines): 800 × level
  - Soft drop: +1 point per cell
  - Hard drop: +2 points per cell
- **Leveling**: Every 10 lines cleared increases the level and fall speed
- **Game Over**: When pieces reach the top of the board

## File Structure

```
tetris/
├── main.py          # Main game loop and rendering
├── game.py          # Core game logic and board management
├── tetromino.py     # Tetromino pieces and their rotations
├── controls.py      # Input handling and control mapping
└── README.md        # This file
```

## Code Architecture

The game is built with a modular architecture:

- **`controls.py`**: Handles all keyboard input and maps keys to game actions
- **`tetromino.py`**: Defines the 7 tetromino types with their shapes, colors, and rotations
- **`game.py`**: Contains the core game logic including collision detection, line clearing, and scoring
- **`main.py`**: Manages the pygame window, rendering, and main game loop

## Customization

The game is designed to be easily customizable:

- **Controls**: Modify key mappings in `controls.py`
- **Gameplay**: Adjust fall speed, scoring, or board size in `game.py`
- **Visuals**: Change colors, block size, or add effects in `main.py`
- **Pieces**: Add new tetromino types or modify existing ones in `tetromino.py`

## License

This project is open source and available under the MIT License.
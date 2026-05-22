# Fill Algorithms Visualization

This repository contains two interactive OpenGL visualizations for fill algorithms using `pygame` and `PyOpenGL`.

## Files

- `BoundaryFill.py`
  - Generates random enclosed boundary shapes on a grid.
  - Uses a queue-based boundary fill algorithm to fill interior regions when the user clicks inside a region.
  - Press `SPACE` to regenerate the random boundaries.

- `FloodFill.py`
  - Creates a random grid of colored cells.
  - Uses a queue-based flood fill algorithm to fill all adjacent cells of the same color when the user clicks a cell.
  - Press `SPACE` to reset the grid with a new random pattern.

## Requirements

- Python 3.8+ (or compatible version)
- `pygame`
- `PyOpenGL`

## Installation

Install the required Python packages with:

```bash
pip install pygame PyOpenGL
```

## Usage

Run either script from the folder containing the files:

```bash
python BoundaryFill.py
```

or

```bash
python FloodFill.py
```

## Controls

- Left click inside the window to start the fill algorithm.
- Press `SPACE` to regenerate or reset the grid.
- Close the window to exit.

## Notes

- The visualizations run using an OpenGL context provided by `pygame`.
- The fill logic is animated by processing a few cells each frame, creating a visible spread effect.

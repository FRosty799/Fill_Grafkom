import pygame
from pygame.locals import *
from OpenGL.GL import *
import random
import time

# --- CONFIGURATION CONSTANTS ---
GRID_ROWS = 20
GRID_COLS = 20
CELL_SIZE = 30  # Pixels per grid square
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE

# --- COLOR VALUES (RGB Normalized 0.0 - 1.0) ---
PALETTE = [
    [0.15, 0.15, 0.20],  # 0: Dark Charcoal (Empty/Background)
    [0.70, 0.20, 0.20],  # 1: Ruby Red (Walls/Obstacles)
    [0.20, 0.60, 0.30],  # 2: Emerald Green (Target Flood Zones)
]
FLOOD_COLOR = [0.20, 0.50, 0.90]  # Light Blue for the actively spreading fill

# --- GLOBAL STATE ---
grid = [[random.choice([0, 1, 2]) for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
flood_queue = []
target_color_idx = -1

def init_opengl():
    """Sets up a simple 2D orthographic projection viewport."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Establish standard 2D pixel coordinates (0,0 is Top-Left)
    glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_filled_square(x, y, size, color):
    """Renders a flat, filled quad on screen using standard OpenGL geometry primitives."""
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + size, y)
    glVertex2f(x + size, y + size)
    glVertex2f(x, y + size)
    glEnd()

def draw_grid_lines():
    """Draws wireframe outlines over the cells so the grid structure is clearly visible."""
    glColor3f(0.3, 0.3, 0.3)  # Muted grey lines
    glLineWidth(1.0)
    glBegin(GL_LINES)
    # Vertical grid line sweeps
    for c in range(GRID_COLS + 1):
        glVertex2f(c * CELL_SIZE, 0)
        glVertex2f(c * CELL_SIZE, WINDOW_HEIGHT)
    # Horizontal grid line sweeps
    for r in range(GRID_ROWS + 1):
        glVertex2f(0, r * CELL_SIZE)
        glVertex2f(WINDOW_WIDTH, r * CELL_SIZE)
    glEnd()

def render():
    """Main rendering loop clearing buffers and iterating through the data matrix."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw all matrix cells based on their current color state
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            val = grid[r][c]
            # Check if this cell is a static palette color or overridden by our active flood int marker (9)
            color = FLOOD_COLOR if val == 9 else PALETTE[val]
            draw_filled_square(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, color)

    draw_grid_lines()
    pygame.display.flip()

def start_flood_fill(click_x, click_y):
    """Translates screen pixel coordinates to matrix indices and starts the queue."""
    global flood_queue, target_color_idx
    
    col = click_x // CELL_SIZE
    row = click_y // CELL_SIZE
    
    # Structural boundaries safety catch
    if not (0 <= row < GRID_ROWS and 0 <= col < GRID_COLS):
        return
        
    target_color_idx = grid[row][col]
    
    # Do not flood fill if clicking a cell that's already the flood color
    if target_color_idx == 9:
        return
        
    # Seed the queue with our starting position
    flood_queue = [(row, col)]

def update_flood_step():
    """Processes a small chunk of cells per frame to animate the flood fill cleanly."""
    global flood_queue, grid, target_color_idx
    
    if not flood_queue:
        return

    # Process 2 cells per frame step so the animation crawls visibly across the screen
    for _ in range(min(2, len(flood_queue))):
        r, c = flood_queue.pop(0)
        
        if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS and grid[r][c] == target_color_idx:
            grid[r][c] = 9  # Mark cell as flooded
            
            # Queue 4-directional updates
            flood_queue.append((r + 1, c))
            flood_queue.append((r - 1, c))
            flood_queue.append((r, c + 1))
            flood_queue.append((r, c - 1))

# --- MAIN EXECUTION ENGINE ---
def main():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL Interactive Flood Fill (Click Grid to Flood!)")
    
    init_opengl()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Mouse Click
                    mx, my = pygame.mouse.get_pos()
                    start_flood_fill(mx, my)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Reset grid on Spacebar press
                    global grid, flood_queue
                    grid = [[random.choice([0, 1, 2]) for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
                    flood_queue = []

        # Advance the animation step and redraw frames
        update_flood_step()
        render()
        clock.tick(60)  # Cap performance safely at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
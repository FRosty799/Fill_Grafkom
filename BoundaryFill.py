import pygame
from pygame.locals import *
from OpenGL.GL import *
import random

# --- CONFIGURATION CONSTANTS ---
GRID_ROWS = 25
GRID_COLS = 25
CELL_SIZE = 25
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE

# --- MATRIX CODES ---
EMPTY = 0
BOUNDARY = 1
FILLED = 9

# --- COLOR PALETTE ---
COLOR_EMPTY = [0.10, 0.10, 0.12]     # Dark Grey Canvas
COLOR_BOUNDARY = [1.00, 1.00, 1.00]  # Bright White Walls
COLOR_FILLED = [0.20, 0.50, 0.90]    # Light Blue Ink

# --- GLOBAL STATE ---
grid = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
fill_queue = []

def generate_random_boundaries():
    """Generates a randomized set of enclosed rooms and outlines on the canvas."""
    global grid, fill_queue
    fill_queue = []
    
    # Reset grid to pure empty space
    grid = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    
    # 1. Always build a hard outer frame around the window edges
    for c in range(GRID_COLS):
        grid[0][c] = BOUNDARY
        grid[GRID_ROWS - 1][c] = BOUNDARY
    for r in range(GRID_ROWS):
        grid[r][0] = BOUNDARY
        grid[r][GRID_COLS - 1] = BOUNDARY

    # 2. Scatter 4 to 7 random enclosed boxes across the interior
    num_boxes = random.randint(4, 7)
    for _ in range(num_boxes):
        # Generate random top-left corner coordinates
        start_r = random.randint(2, GRID_ROWS - 8)
        start_c = random.randint(2, GRID_COLS - 8)
        
        # Generate random width and height for this specific box
        box_h = random.randint(4, 8)
        box_w = random.randint(4, 8)
        
        # Draw the top and bottom solid horizontal boundaries
        for c in range(start_c, start_c + box_w):
            if c < GRID_COLS - 1:
                grid[start_r][c] = BOUNDARY
                grid[min(start_r + box_h - 1, GRID_ROWS - 2)][c] = BOUNDARY
                
        # Draw the left and right solid vertical boundaries
        for r in range(start_r, start_r + box_h):
            if r < GRID_ROWS - 1:
                grid[r][start_c] = BOUNDARY
                grid[r][min(start_c + box_w - 1, GRID_COLS - 2)] = BOUNDARY

def init_opengl():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_quad(x, y, size, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + size, y)
    glVertex2f(x + size, y + size)
    glVertex2f(x, y + size)
    glEnd()

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            val = grid[r][c]
            if val == BOUNDARY:
                color = COLOR_BOUNDARY
            elif val == FILLED:
                color = COLOR_FILLED
            else:
                color = COLOR_EMPTY
            draw_quad(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, color)

    pygame.display.flip()

def start_boundary_fill(mx, my):
    global fill_queue
    col = mx // CELL_SIZE
    row = my // CELL_SIZE
    
    if not (0 <= row < GRID_ROWS and 0 <= col < GRID_COLS):
        return
    
    # Boundary logic safeguard: do not pick a boundary cell or an already filled cell
    if grid[row][col] == BOUNDARY or grid[row][col] == FILLED:
        return
        
    fill_queue = [(row, col)]

def update_fill_animation():
    global fill_queue, grid
    
    if not fill_queue:
        return

    # Process 5 cells per loop cycle to quickly navigate the complex rooms
    for _ in range(min(5, len(fill_queue))):
        if not fill_queue: 
            break
        r, c = fill_queue.pop(0)
        
        if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
            # Check condition: Is it a wall or already painted?
            if grid[r][c] != BOUNDARY and grid[r][c] != FILLED:
                grid[r][c] = FILLED
                
                # Check all 4 surrounding neighbors
                fill_queue.append((r + 1, c))
                fill_queue.append((r - 1, c))
                fill_queue.append((r, c + 1))
                fill_queue.append((r, c - 1))

def main():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Random Boundary Fill (Click Inside/Outside Shapes, SPACE to reshuffle)")
    
    init_opengl()
    generate_random_boundaries()
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click
                    mx, my = pygame.mouse.get_pos()
                    start_boundary_fill(mx, my)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generate_random_boundaries()

        update_fill_animation()
        render()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
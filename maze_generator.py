import pygame
from random import choice

# initializing pygame
pygame.init()

# defining required variables
screen_width = 1000
screen_height = 600
TILE = tile_size = 50
RES = screen_width, screen_height
cols, rows = screen_width // TILE, screen_height // TILE
clockobject = pygame.time.Clock()
fps = 60

# setting up window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('maze generator') # title

# maze creation
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    # method to highlight current cell
    def draw_current_cell(self):
        x, y = self.x* TILE, self.y* TILE
        pygame.draw.rect(screen, pygame.Color('brown'), (x+2, y+2, TILE-2, TILE-2))

    # method to drawing line and cell
    def draw(self):
        x, y = self.x * TILE, self.y * TILE

        # fill visited cell with black
        if self.visited:
            pygame.draw.rect(screen, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y + TILE), (x , y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + TILE), (x, y), self.thickness)

    # getting cell coordinates
    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
        if self.walls['right']:
            rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
        if self.walls['bottom']:
            rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
        if self.walls['left']:
            rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
        return rects

    # cheking cell inside window
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    # cheking if neighbors cell are visited
    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False # return non visited neighbor cell

# function to remove wall in path
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze(show_maze_generation, show_out_path):
    # defining required variables
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    out_path = [(0, 0)]
    run = True

    while run:
        clockobject.tick(fps) # fps setting

        [cell.draw() for cell in grid_cells] # drawing cells
    
        # generating maze
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()

        # drawing maze generation
        stack_len = len(stack)
        if show_maze_generation:
            [pygame.draw.rect(screen, (255, 0, 0), (cell.x*TILE+5, cell.y*TILE+5,
                TILE-10, TILE-10), border_radius=12) for cell in stack]

        # drawing out path
        if show_out_path:
            if len(out_path) == 1: # getting correct out path
                stack_last = stack[-1]
                if stack_last.x == (screen_width//tile_size)-1 and stack_last.y == (screen_height//tile_size)-1:
                    out_path = [(i.x, i.y) for i in stack]
            
            if stack_len == 0:
                [pygame.draw.rect(screen, (0, 255, 0), (x*TILE+5, y*TILE+5,
                        TILE-10, TILE-10), border_radius=12) for x, y in out_path]

        # window event checking
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update() # updating window

    pygame.quit()

if __name__ == '__main__':
    generate_maze(show_maze_generation=True, show_out_path=True)
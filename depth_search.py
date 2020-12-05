import random
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.


class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze_map[x][y]

    def get_struct(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['w' * (self.nx * 4 + 1)]
        for y in range(self.ny):
            maze_row = ['w']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append('xxx|')
                else:
                    maze_row.append('xxxx')
            maze_rows.append(''.join(maze_row))
            maze_row = ['w']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('----')
                else:
                    maze_row.append('xxx|')
            maze_rows.append(''.join(maze_row))
        return maze_rows

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['w' * (self.nx*4+1)]
        for y in range(self.ny):
            maze_row = ['w']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append('xxx|')
                else:
                    maze_row.append('xxxx')
            maze_rows.append(''.join(maze_row))
            maze_row = ['w']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('----')
                else:
                    maze_row.append('xxx|')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def return_img2(self):
        maze_struct = self.get_struct()
        height, width = len(maze_struct), len(maze_struct[0])
        print(height, width)
        img = np.full((height, width), 0)
        for y in range(height):
            for x in range(width):
                if maze_struct[y][x] == 'w' or maze_struct[y][x] == '-' or maze_struct[y][x] == '|':
                    img[y,x] = 0
                elif maze_struct[y][x] == 'x':
                    img[y,x] = 255
        return img

    def return_img(self):
        aspect_ratio = self.nx/self.ny
        height = self.ny
        width = int(height * aspect_ratio)
        padding = 10
        scy, scx = height/self.ny, width/self.nx

        img = np.full((height, width), 0)
        print(img)
        for y in range(1,self.ny-1,2):
            for x in range(1,self.nx-1,2):
                if self.maze_map[x][y].walls['E']:
                    img[y,x] = 255
                    #img[y,x+1] = 0
                else:
                    continue
                    #img[y,x] = 255
                    #img[y,x+1] = 255
            for x in range(1,self.nx-1,2):
                if self.maze_map[x][y].walls['S']:
                    img[y+1, x] = 0
                    img[y+1, x+1] = 0
                else:
                    img[y+1, x] = 255
                    img[y+1, x+1] = 0
        '''
        for y in range(self.ny):
            img[y,0] = 0
            img[y, self.nx - 1] = 0
        for x in range(self.nx):
            img[0,x] = 0
            img[self.ny-1, x] = 0
        '''
        print(img)
        return img

    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1


if __name__ == "__main__":
    nx, ny = 50, 50
    # Maze entry position
    ix, iy = 0, 0

    maze = Maze(nx, ny, ix, iy)
    maze.make_maze()

    print(maze)
    img = maze.return_img2()
    plt.imshow(img, 'gray')
    cv.imwrite('maze.png', img)
    plt.show()
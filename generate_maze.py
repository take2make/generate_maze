import random
import matplotlib.pyplot as plt
import numpy as np

# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/


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

    def get_struct(self, padding=10):
        """Return a (crude) string representation of the maze."""
        maze_rows = ['w' * (self.nx * padding * 2 + padding)]
        for p in range(padding - 1):
            maze_rows.append(''.join(['w' * (self.nx * padding * 2 + padding)]))
        for y in range(self.ny):
            for i in range(padding):
                maze_row = ['w' * padding]
                for x in range(self.nx):
                    if self.maze_map[x][y].walls['E']:
                        maze_row.append(''.join(['x' * padding + '|' * padding]))
                    else:
                        maze_row.append(''.join(['x' * padding * 2]))
                maze_rows.append(''.join(maze_row))
            for j in range(padding):
                maze_row = ['w' * padding]
                for x in range(self.nx):
                    if self.maze_map[x][y].walls['S']:
                        maze_row.append(''.join(['-' * padding * 2]))
                    else:
                        maze_row.append(''.join(['x' * padding + '|' * padding]))
                maze_rows.append(''.join(maze_row))
        return maze_rows

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

    def return_img(self, padding=10):
        maze_struct = self.get_struct(padding)
        height, width = len(maze_struct), len(maze_struct[0])
        print(height, width)
        img = np.full((height, width), 0)
        for y in range(height):
            for x in range(width):
                if maze_struct[y][x] == 'w' or maze_struct[y][x] == '-' or maze_struct[y][x] == '|':
                    img[x,y] = 0
                elif maze_struct[y][x] == 'x':
                    img[x,y] = 255
        for y in range(padding, padding*2):
            for x in range(self.iy + padding):
                img[x,y] = 170
        for y in range(height - padding, height):
            for x in range(width - padding*2, width-padding):
                img[x,y] = 170
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
    nx, ny = 20, 20
    # Maze entry position
    ix, iy = 0, 0

    maze = Maze(nx, ny, ix, iy)
    maze.make_maze()

    print(maze)
    img = maze.return_img(padding=10)
    fig = plt.imshow(img, 'gray')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig('maze2.png')
    #plt.show()
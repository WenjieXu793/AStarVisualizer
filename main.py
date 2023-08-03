import pygame
import math
from queue import PriorityQueue

rows = int(input("Input number of rows in Grid: "))
columns = int(input("Input number of columns in Grid: "))
print("Would you like to use the Manhattan distance or the Euclidian distance for the heuristic function?")
h = str(input("Input lowercase \"m\" for Manhattan distance and \"e\" for Euclidian distance(m/e): "))
while h!="m" and h!="e":
    h = str(input("Please enter either \"m\" or \"e\": "))
squareSide = 12
Window = pygame.display.set_mode((columns*squareSide, rows*squareSide))
pygame.display.set_caption("This is an A* Pathfinding Algorithm Visualizer")

black = (0, 0, 0)
white = (255, 255, 255)
grey = (120, 120, 120)
red = (255, 0, 0)
green = (0, 255, 0)
darkgreen = (0, 128, 0)
cyan = (68, 230, 210)
yellow = (255, 255, 0)
orange = (240, 150, 0)
purple = (100, 0, 100)

class Square:
    def __init__(self, row, column, width, height, total_rows, total_columns):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * height
        self.color = black
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_columns = total_columns

    def getPos(self):
        return self.row, self.column

    def isClosed(self):
        return (self.color==orange)

    def isOpen(self):
        return (self.color==red)

    def isBarrier(self):
        return (self.color == white)

    def isStart(self):
        return (self.color == green)

    def isTarget(self):
        return (self.color == purple)

    def reset(self):
        self.color = black

    def makeClosed(self):
        self.color = orange

    def makeOpen(self):
        self.color = red

    def makeBarrier(self):
        self.color = white

    def makeStart(self):
        self.color = green

    def makeTarget(self):
        self.color = purple

    def makePath(self,count):
        if count%2==0:
            self.color = cyan
        else:
            self.color = darkgreen

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def updateNeighbors(self, grid):
        self.neighbors = []
        if self.row<self.total_rows - 1 and not grid[self.row+1][self.column].isBarrier():
            self.neighbors.append(grid[self.row+1][self.column])
        if self.row>0 and not grid[self.row-1][self.column].isBarrier():
            self.neighbors.append(grid[self.row-1][self.column])
        if self.column<self.total_columns - 1 and not grid[self.row][self.column+1].isBarrier():
            self.neighbors.append(grid[self.row][self.column+1])
        if self.column>0 and not grid[self.row][self.column-1].isBarrier():
            self.neighbors.append(grid[self.row][self.column-1])

    def __lt__(self, other):
        return False

def heuristic(square1, square2):
    x1, y1 = square1
    x2, y2 = square2
    if h == "m":
        return abs(x1 - x2) + abs(y1 - y2)
    if h=="e":
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def path(edgeTo, curr, draw):
    c = 0
    while curr in edgeTo:
        curr = edgeTo[curr]
        if not curr.isStart() and not curr.isTarget():
            curr.makePath(c)
            c+=1
        draw()

def algorithm(draw, grid, start, target):
    counter = 0
    pq = PriorityQueue()
    pq.put((0, counter, start))
    edgeTo = {}
    gval = {square: float("inf") for row in grid for square in row}
    gval[start] = 0
    fval = {square: float("inf") for row in grid for square in row}
    fval[start] = heuristic(start.getPos(), target.getPos())
    pq_hash = {start}

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        curr = pq.get()[2]
        pq_hash.remove(curr)

        if curr==target:
            path(edgeTo, target, draw)
            return True

        for neighbor in curr.neighbors:
            tempG = gval[curr] + 1
            if tempG < gval[neighbor]:
                edgeTo[neighbor] = curr
                gval[neighbor] = tempG
                fval[neighbor] = tempG + heuristic(neighbor.getPos(), target.getPos())
                if neighbor not in pq_hash:
                    counter+=1
                    pq.put((fval[neighbor], counter, neighbor))
                    pq_hash.add(neighbor)
                    if not neighbor.isTarget():
                        neighbor.makeOpen()
        draw()

        if curr != start:
            curr.makeClosed()

    return False

def makeGrid(columns, rows, width):
    grid = []
    gap = width//columns
    for i in range(columns):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, gap, columns, rows)
            grid[i].append(square)
    return grid

def drawGrid(window, columns, rows, width, height):
    gap = width//columns
    for i in range(rows):
        pygame.draw.line(window, grey, (0, i*gap), (width, i * gap))
    for i in range(width):
        pygame.draw.line(window, grey, (i * gap, 0), (i * gap, height))

def draw(window, grid, columns, rows, width, height):
    window.fill(black)
    for row in grid:
        for square in row:
            square.draw(window)
    drawGrid(window, columns, rows, width, height)
    pygame.display.update()

def mousePos(pos, columns, width):
    gap = width//columns
    y, x = pos
    row = y//gap
    column = x//gap
    return row, column

def main(window, columns, rows):
    start = None
    target = None
    width = columns*squareSide
    height = rows*squareSide
    grid = makeGrid(columns, rows, width)
    started = False
    begin = True
    while begin:
        draw(window, grid, columns, rows, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                begin = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, column = mousePos(pos, columns, width)
                square = grid[row][column]
                if not start and square != target:
                    square.makeStart()
                    start = square
                elif not target and square != start:
                    square.makeTarget()
                    target = square
                elif square != target and square != start:
                    square.makeBarrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, column = mousePos(pos, columns, width)
                square = grid[row][column]
                square.reset()
                if square == start:
                    start = None
                elif square == target:
                    target = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for square in row:
                            square.updateNeighbors(grid)

                    algorithm(lambda: draw(window, grid, columns, rows, width, height), grid, start, target)
                if event.key == pygame.K_q:
                    start = None
                    target = None
                    grid = makeGrid(columns, rows, width)
    pygame.quit()



main(Window, columns, rows)
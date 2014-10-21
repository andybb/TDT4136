# Subtask A-3
# Solving with BFS
__authors__ = 'Stein-Otto Svorstol and Andreas Drivenes'

import heapq
from collections import deque

class Cell(object):
    def __init__(self, x, y, cost, reachable):
        self.x = x
        self.y = y
        self.cost = cost
        self.reachable = reachable
        self.parent = None
        self.g = 0
        self.f = 0
        self.h = 0


    def __repr__(self):
        return self.x, self.y

    def __lt__(self, other):
        return self.f < other.f

# # is wall
# A is start
# B is goal
# . is empty cell


class AStar(object):
    def __init__(self, newBoardname):
        self.opened = deque() # Visited nodes
        self.closed = set()
        self.cells = []
        self.gridHeight = 0 # Set in initGrid
        self.gridWidth = 0
        self.matrix = []
        self.boardname = newBoardname
        self.initGrid()

    def readFile(self, filename):
        #Goes over file and creates a matrix of it
        file = open(filename, 'r')
        matrix = []
        for line in file:
            lineMatrix = []
            for char in line:
                if(char == '\n'): # We don't want the linebreak in our matrix.
                    break
                lineMatrix.append(char)
            matrix.append(lineMatrix)
        return matrix

    def getAB(self, matrix):
        # Goes over a matrix and returns location of A and B
        A, B = (0,0), (0,0)
        for y in range(0, len(matrix)):
            for x in range(0, len(matrix[y])):
                if(matrix[y][x] == 'A'):
                    A = (x, y)
                elif (matrix[y][x] == 'B'):
                    B = (x, y)
        return A, B

    def getWalls(self, matrix):
        # Goes over a matrix and returns coordinates for the walls as a list
        walls = []
        for y in range(0, len(matrix)):
            for x in range(0, len(matrix[y])):
                if(matrix[y][x] == '#'):
                    walls.append((x, y))
        return walls

    def getCellCost(self, x, y):
        c = self.matrix[y][x]
        #Map the cost according to cell type
        if(c == 'w'):
            return 100
        elif(c == 'm'):
            return 50
        elif(c == 'f'):
            return 10
        elif(c == 'g'):
            return 5
        else:
         return 1


    def getHeuristic(self, cell):
        #Calculate the Manhattan Distance between a cell and the goal cell
        #This will serve as our heuristic for the A* Algorithm
        return (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def getCell(self, x, y):
        return self.cells[x * self.gridHeight + y]

    def updateCell(self, neighbor, cell):
        #The cost to get to this cell
        neighbor.g = cell.g + cell.cost
        #The heuristic
        neighbor.h = self.getHeuristic(neighbor)
        neighbor.parent = cell
        neighbor.f = neighbor.g + neighbor.h

    def getNeighbors(self, cell):
        neighbors = []
        #Go right
        if(cell.x < self.gridWidth - 1):
            neighbors.append(self.getCell(cell.x + 1, cell.y))
        #Go left
        if(cell.y > 0):
            neighbors.append(self.getCell(cell.x, cell.y - 1))
        #Go up
        if(cell.x > 0):
            neighbors.append(self.getCell(cell.x - 1, cell.y))
        #Go down
        if(cell.y < self.gridHeight - 1):
            neighbors.append(self.getCell(cell.x, cell.y + 1))
        return neighbors


    def initGrid(self):
        # First get our coordinates:
        self.matrix = self.readFile(self.boardname)
        walls = self.getWalls(self.matrix)
        start, end = self.getAB(self.matrix)

        # Set the values for the size of the grid
        self.gridHeight = len(self.matrix)
        self.gridWidth = len(self.matrix[0])

        # Let's make some cells
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                 # If location is a wall, we cannot go there.
                reachable = False if (x, y) in walls else True
                self.cells.append(Cell(x, y, self.getCellCost(x, y), reachable))
        self.start = self.getCell(start[0], start[1])
        self.end = self.getCell(end[0], end[1])

    def displayPath(self):
        cell = self.end

        #Display * for the open nodes
        for oCell in self.opened:
            self.matrix[oCell.y][oCell.x] = '*'

        #Display x for the closed nodes
        for cCell in self.closed:
            matrixCell = self.matrix[cCell.y][cCell.x]
            if matrixCell != 'A' and matrixCell != 'B':
                self.matrix[cCell.y][cCell.x] = 'x' 

        #Display o for the shortest path to the goal
        while cell.parent is not self.start:
            cell = cell.parent
            self.matrix[cell.y][cell.x] = 'o'

        board = ''
        for y in range(0, len(self.matrix)):
            row = ''
            for x in range(0, len(self.matrix[y])):
                row += self.matrix[y][x]
            board += row + '\n'
        print(board)


    def solve(self):
        #This is our implementation of the BFS algorithm
        #Push the start cell to the list of open nodes
        #We now treat opened as a FIFO queue and use popleft and appendleft
        self.opened.appendleft(self.start)
        while self.opened:
            cell = self.opened.popleft()
            self.closed.add(cell)

            if cell is self.end:
                return self.displayPath()

            #Loop through all the neighbor nodes 
            for neighbor in self.getNeighbors(cell):
                if neighbor.reachable and neighbor not in self.closed:
                    if neighbor in self.opened:
                        if neighbor.g > cell.g + neighbor.cost:
                            self.updateCell(neighbor, cell)
                    else:
                        self.updateCell(neighbor, cell)
                        self.opened.appendleft(neighbor)


def main():
    boardRoot = 'boards/board-'
    boards = ['1-1', '1-2', '1-3', '1-4', '2-1', '2-2', '2-3', '2-4']
    for board in boards:
        boardName = boardRoot + board + '.txt'
        print(boardName)
        thing = AStar(boardName).solve()

# main()
thing = AStar('boards/board-2-3.txt').solve()
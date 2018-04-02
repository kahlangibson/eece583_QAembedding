from random import *

class Cell(object):
    """ Cell object with x,y position
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circuit:
    def __init__(self, f):
        [self.numCells, self.numNets, self.ny, self.nx] = [int(s) for s in f.readline().split()]

        self.nets = []
        self.costs = []
        for _ in range(self.numNets):
            line = f.readline().split()
            if len([s for s in line]) is 0:
                # empty line, read next
                line = f.readline().split()
            # source of net
            net = [int(line[1])]
            # sinks of net
            net.append([int(s) for s in line[2:]])
            self.nets.append(net)
            self.costs.append(0)
        f.close()

        self.grid = []
        for _ in range(self.ny):
            row = []
            for _ in range(self.nx):
                row.append(' ')
            self.grid.append(row)

        self.cost = 0
        self.cells = []

        self.init_place()

    def is_empty(self, x, y):
        """ Checks the status of the cell position x,y
        returns:
            False if the cell is not empty or x,y is not in the grid range
            True otherwise
        """
        if x in range(self.nx) and y in range(self.ny):
            if self.grid[y][x] == ' ':
                return True
        return False

    def put_cell(self, x, y, num):
        """ Places cell #num on the array at empty position x,y
        sets:
            - self.grid at x,y, and updates image with initial placement
        returns:
            False if the cell fails not_empty
            True otherwise
        :param x: x value of cell
        :param y: y value of cell
        """
        if self.is_empty(x,y):
            self.grid[y][x] = num
            return True
        return False

    def init_place(self):
        """ Places cells on the array initially
        assumes:
            - nothing has been placed before
        sets:
            - self.grid, and updates image with initial placement
            - self.cost
        asserts:
            - if failure to place cell in grid (put_cell returns False)
            - if failure to calculate cost (calc_cost returns False)
        """
        for i in range(self.numCells):
            x = randint(0,self.nx)
            y = randint(0,self.ny)
            while not self.is_empty(x,y):
                x = randint(0, self.nx)
                y = randint(0, self.ny)
            assert self.put_cell(x, y, i) is True
            self.cells.append(Cell(x,y))

        assert self.calc_cost() is True

    def switch(self, x1, y1, x2, y2):
        """ Switches cells specified by x1,y1 and x2,y2
        :param x1: x coordinate of cell1
        :param y1: y coordinate of cell1
        :param x2: x coordinate of cell2
        :param y2: y coordinate of cell2
        assumes:
            - at least one cell is not empty
        sets:
            - self.grid, and updates image with new placement
            - self.cells, and updates new position for moved cell
            - self.cost
        asserts:
            - if failure to switch cells (both cells are empty)
        """
        # both positions should not be empty
        assert (self.is_empty(x1, y1) is not True) or (self.is_empty(x2, y2) is not True)
        # x1,y1 is empty
        if self.is_empty(x1, y1):
            self.grid[y1][x1] = self.grid[y2][x2]
            self.cells[self.grid[y2][x2]].x = x1
            self.cells[self.grid[y2][x2]].y = y1
            self.grid[y2][x2] = ' '
            self.update_cost(self.grid[y1][x1])
        # x2,y2 is empty
        elif self.is_empty(x2, y2):
            self.grid[y2][x2] = self.grid[y1][x1]
            self.cells[self.grid[y1][x1]].x = x2
            self.cells[self.grid[y1][x1]].y = y2
            self.grid[y1][x1] = ' '
            self.update_cost(self.grid[y2][x2])
        else:
            n = self.grid[y2][x2]
            self.grid[y2][x2] = self.grid[y1][x1]
            self.cells[self.grid[y1][x1]].x = x2
            self.cells[self.grid[y1][x1]].y = y2
            self.grid[y1][x1] = n
            self.cells[n].x = x1
            self.cells[n].y = y1
            self.update_cost(self.grid[y1][x1])
            self.update_cost(self.grid[y2][x2])

    def compare_switch_cost(self, x1, y1, x2, y2):
        """ Compares the cost functions of the switching of cells at x1,y1 and x2,y2
        :param x1: x coordinate of cell1
        :param y1: y coordinate of cell1
        :param x2: x coordinate of cell2
        :param y2: y coordinate of cell2
        :return: the difference in cost function
        """
        cost = self.cost
        self.switch(x1,y1,x2,y2)
        deltaC = self.cost - cost
        return deltaC

    def update_cost(self, id):
        """ Calculates the updated cost given a moved net with index id, to prevent recalculating full cost
        :param: id: the if of the source/sink cell that was moved
        assumes:
            - valid net list in self.nets
        sets:
            - self.cost
        :return: True once complete
        """
        cost = 0
        for i, [source, sinks] in enumerate(self.nets):
            if id == source:
                self.costs[i] = self.calc_half_perimeter(source, sinks)
                cost += self.costs[i]
            elif id in sinks:
                self.costs[i] = self.calc_half_perimeter(source, sinks)
                cost += self.costs[i]
            else:
                cost += self.costs[i]

        self.cost = cost
        return True

    def calc_cost(self):
        """ Calculates the initial cost for all nets
        assumes:
            - valid net list in self.nets
        sets:
            - self.cost
        :return: True once complete
        """
        cost = 0
        for i,[source, sinks] in enumerate(self.nets):
            self.costs[i] = self.calc_half_perimeter(source, sinks)
            cost += self.costs[i]
        self.cost = cost
        return True

    def calc_half_perimeter(self, source, sinks):
        """ Calculates the half perimeter smallest bounding box cost of a net
        assumes:
            - valid cell positions in source, sinks
        asserts:
            - if failure to calculate cost (any cell x,y not in grid range)
        :param source: index of the source cell
        :param sinks: indices of the sink cells
        :return: half-perimeter cost of the net
        """
        deltax = 0
        deltay = 0
        assert self.cells[source].x in range(self.nx) and self.cells[source].y in range(self.ny)
        for sink in sinks:
            assert self.cells[sink].x in range(self.nx) and self.cells[sink].y in range(self.ny)
            dx = abs(self.cells[source].x - self.cells[sink].x)
            if dx > deltax:
                deltax = dx
            dy = abs(self.cells[source].y - self.cells[sink].y)
            if dy > deltay:
                deltay = dy
        return deltax + deltay


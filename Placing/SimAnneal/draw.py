from Tkinter import *
import Tkinter as tk
from math import *
from random import *
from circuit import *
from time import sleep

class draw(Circuit):
    def __init__(self, parent, startT, beta, exitRate, runWith0, f):
        Circuit.__init__(self, f)
        self.myParent = parent
        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()
        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)
        # set this to True to *not* run animation
        self.fast = False

        self.cellwidth = 0
        self.cellheight = 0
        self.rect = {}
        self.text = {}
        self.celltext = {}
        self.lines = {}
        self.costy = 0
        self.costtext = 0
        self.tempText = None

        self.startT = startT
        self.beta = beta
        self.exitRate = exitRate
        self.runWith0 = True
        self.n = 10*int(pow(self.numCells, (4./3.)))

        self.num_accepted = 0.
        self.total_proposed = 0.

        # things that happen to init circuit
        self.make(self.ny, self.nx)
        for each in self.cells:
            self.place(each.x, each.y, self.grid[each.y][each.x])
        for source, sinks in self.nets:
            for sink in sinks:
                self.draw_net(source, sink, self.cells[source].x, self.cells[source].y, self.cells[sink].x,
                              self.cells[sink].y)
        self.drawcost(self.cost)

    def runSimAnneal(self):
        temp = self.startT
        if not self.fast:
            sleep(0.25)
            self.drawtemp(temp)
            self.myCanvas.update()

        self.tempLoop(temp)

        if self.fast:
            self.clear_nets()
            for source, sinks in self.nets:
                for sink in sinks:
                    self.draw_net(source, sink, self.cells[source].x, self.cells[source].y, self.cells[sink].x,
                                  self.cells[sink].y)
            self.drawcost(self.cost)
            for each in self.celltext:
                self.myCanvas.delete(self.celltext[each])
            for cell in self.cells:
                self.place(cell.x, cell.y, self.grid[cell.y][cell.x])

    def tempLoop(self, temp):
        self.num_accepted = 0.
        self.total_proposed = 0.
        for _ in range(self.n):
            self.nLoop(temp)
        temp = temp * self.beta
        if not self.fast:
            # update nets
            sleep(0.0001)
            self.drawtemp(temp)
            self.myCanvas.update()
        if self.num_accepted / self.total_proposed > self.exitRate:
            self.tempLoop(temp)
        else:
            for _ in range(self.n):
                self.nLoop(0)

    def nLoop(self, temp):
        """
        :param temp: temperature at which to perform simulated annealing
        """
        if not self.fast:
            sleep(0.0001)
        self.total_proposed += 1.
        # randomly choose 2 cells
        # pick a cell from list
        c = sample(self.cells,1)[0]
        x1 = c.x
        y1 = c.y
        # randomly pick another position - may be cell, may be empty
        [x2, y2] = sample(range(self.nx), 1) + sample(range(self.ny), 1)
        if not self.fast:
            self.pick(x1, y1, True)
            self.pick(x2, y2, True)
        # switch and calculate delta cost
        deltaC = self.compare_switch_cost(x1, y1, x2, y2)
        if not self.fast:
            self.drawswitch(x1, y1, self.grid[y1][x1], x2, y2, self.grid[y2][x2])
            self.drawcost(self.cost)
        # generate random number
        r = random()
        # if random number is gt or eq to probability, switch back to original
        if temp is not 0:
            if r >= exp(-deltaC / temp):
                self.switch(x1, y1, x2, y2)
                if not self.fast:
                    self.drawswitch(x1, y1, self.grid[y1][x1], x2, y2, self.grid[y2][x2])
                    self.drawcost(self.cost)
                    self.pick(x1, y1, False)
                    self.pick(x2, y2, False)
            else:
                self.num_accepted += 1.
        else:
            if deltaC > 0:
                self.switch(x1, y1, x2, y2)
                if not self.fast:
                    self.drawswitch(x1, y1, self.grid[y1][x1], x2, y2, self.grid[y2][x2])
                    self.drawcost(self.cost)
                    self.pick(x1, y1, False)
                    self.pick(x2, y2, False)
            else:
                self.num_accepted += 1.
        if not self.fast:
            self.myCanvas.update()
            self.unpick(x1,y1)
            self.unpick(x2,y2)

    def delete(self):
        self.myCanvas.delete('all')
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)

    def clear_nets(self):
        for each in self.lines:
            self.myCanvas.delete(self.lines[each])

    def make(self, rows, columns):
        bigger = max(columns, rows)
        self.cellwidth = min(1000/bigger, 50)
        self.cellheight = min(1000/bigger, 50)
        self.buffer = 0.1*min(1000/bigger, 50)

        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,
                                width=(self.cellheight+self.buffer)*columns + self.buffer,
                                height=(self.cellwidth+self.buffer)*rows + self.buffer + 50)
        self.myCanvas.pack(side=tk.RIGHT)

        for x in range(columns):
            for y in range(rows):
                x1 = x * (self.cellwidth + self.buffer) + self.buffer
                y1 = y * (self.cellheight + self.buffer) + self.buffer
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[y, x] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="white")

        self.costy = rows * (self.cellheight + self.buffer) + self.buffer * 3
        self.text[10,self.costy] = self.myCanvas.create_text(20, self.costy, text="Cost:  ")
        self.costtext = self.myCanvas.create_text(1, self.costy, text=0)

    def pick(self, x, y, taken):
        r = self.rect[y,x]
        if taken:
            self.myCanvas.itemconfigure(r, fill="green")
        else:
            self.myCanvas.itemconfigure(r, fill="red")
        self.myCanvas.tag_lower(r)

    def unpick(self, x, y):
        r = self.rect[y,x]
        self.myCanvas.itemconfigure(r, fill="white")
        self.myCanvas.tag_lower(r)

    def drawswitch(self, x1, y1, t1, x2, y2, t2):
        if (x1,y1) in self.celltext:
            self.myCanvas.delete(self.celltext[x1, y1])
        if t1 is not ' ':
            self.place(x1, y1, t1)
        if (x2,y2) in self.celltext:
            self.myCanvas.delete(self.celltext[x2, y2])
        if t2 is not ' ':
            self.place(x2, y2, t2)

    def place(self, x, y, num):
        x1 = x * (self.cellwidth + self.buffer) + self.buffer
        y1 = y * (self.cellheight + self.buffer) + self.buffer
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight
        self.celltext[x, y] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, font=("Helvetica", self.cellheight/2), text=num)

    def remove_net(self, source, sink):
        self.myCanvas.delete(self.lines[source, sink])

    def draw_net(self, source, sink, x1, y1, x2, y2):
        startx = x1 * (self.cellwidth + self.buffer) + self.buffer + self.cellwidth/2
        starty = y1 * (self.cellheight + self.buffer) + self.buffer + self.cellheight/2
        endx = x2 * (self.cellwidth + self.buffer) + self.buffer + self.cellwidth/2
        endy = y2 * (self.cellheight + self.buffer) + self.buffer + self.cellheight/2
        self.lines[source, sink] = self.myCanvas.create_line(startx,starty,endx,endy,arrow=LAST)

    def drawcost(self, cost):
        self.myCanvas.delete(self.costtext)
        self.costtext = self.myCanvas.create_text(75, self.costy, text=cost)

    def drawtemp(self, temp):
        if self.tempText is not None:
            self.myCanvas.delete(self.tempText)
        else:
            self.text[125,self.costy] = self.myCanvas.create_text(125, self.costy, text="Temp:  ")
        self.tempText = self.myCanvas.create_text(175, self.costy, text=int(temp))

# @Override Circuit.compare_switch_cost
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

# @Override Circuit.switch
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

#@Override Circuit.update_cost
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
                if not self.fast:
                    for sink in sinks:
                        self.remove_net(id, sink)
                        self.draw_net(id, sink, self.cells[id].x, self.cells[id].y, self.cells[sink].x,
                                      self.cells[sink].y)
            elif id in sinks:
                self.costs[i] = self.calc_half_perimeter(source, sinks)
                cost += self.costs[i]
                if not self.fast:
                    self.remove_net(source, id)
                    self.draw_net(source, id, self.cells[source].x, self.cells[source].y, self.cells[id].x,
                                  self.cells[id].y)
            else:
                cost += self.costs[i]

        self.cost = cost
        return True
from math import *
from random import *
from circuit import *

class simAnneal(Circuit):
    def __init__(self, startT, beta, exitRate, runWith0, f):
        Circuit.__init__(self, f)
        self.startT = startT
        self.n = 10*int(pow(self.numCells, (4./3.)))
        self.beta = beta
        self.exitRate = exitRate
        self.runWith0 = runWith0
        self.acceptanceRates = []

        self.loop = True

    def runSimAnneal(self):
        temp = self.startT
        while True:
            num_accepted = 0.
            total_proposed = 0.
            for _ in range(self.n):
                total_proposed += 1.
                # randomly choose a cell
                c = sample(self.cells, 1)[0]
                x1 = c.x
                y1 = c.y
                # randomly pick another position - may be cell, may be empty
                [x2, y2] = sample(range(self.nx), 1) + sample(range(self.ny), 1)
                # switch and calculate delta cost
                deltaC = self.compare_switch_cost(x1, y1, x2, y2)
                # generate random number
                r = random()
                # if random number is gt or eq to probability, switch back to original
                if r >= exp(-deltaC/temp):
                    self.switch(x1, y1, x2, y2)
                else:
                    num_accepted += 1.
            print "Temp: " + str(temp) + ", acceptance rate: " + str(num_accepted/total_proposed)
            self.acceptanceRates.append((temp, num_accepted/total_proposed))
            temp = temp * self.beta
            if num_accepted/total_proposed <= self.exitRate:
                if self.runWith0:
                    for _ in range(self.n):
                        while True:
                            [x1, x2, y1, y2] = sample(range(self.nx), 2) + sample(range(self.ny), 2)
                            if not self.is_empty(x1, y1) or not self.is_empty(x2, y2):
                                break
                        # switch and calculate delta cost
                        deltaC = self.compare_switch_cost(x1, y1, x2, y2)
                        # if cost increases, switch back
                        if deltaC > 0:
                            self.switch(x1, y1, x2, y2)
                break

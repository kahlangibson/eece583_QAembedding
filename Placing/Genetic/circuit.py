from __future__ import division
from random import *
from numpy import array, random

class Circuit:
    INIT_SIZE = 30
    POP_SIZE = 30
    NUM_GENERATIONS = 100
    NUM_OFFSPRING = 20

    def __init__(self, f):
        [self.numCells, self.numNets, self.ny, self.nx] = [int(s) for s in f.readline().split()]

        num_ins = int(f.readline().split()[0])
        self.inputs = []
        for _ in range(num_ins):
            line = [int(s) for s in f.readline().split()]
            self.inputs.append(line)

        num_outs = int(f.readline().split()[0])
        self.outputs = []
        for _ in range(num_outs):
            line = [int(s) for s in f.readline().split()]
            self.outputs.append(line)

        self.nets = []
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
        f.close()

        self.reduce_congestion = True
        self.width = 0
        if self.numCells <= self.ny*self.nx/4:
            self.width = 1
        elif self.numCells <= self.ny * self.nx/2:
            self.width = 2
        elif self.numCells <= 3*self.ny * self.nx/4:
            self.width = 3
        else:
            self.width = 4

        self.cells = {}
        self.cost = 0

    def genetic(self):
        """
        """
        # empty population
        population = []
        count = 0
        # initialize population with INIT_SIZE individuals
        for _ in range(self.INIT_SIZE):
            population.append([self.generate_individual(),0])
        # compute individual "fitness"
        population = self.evaluate_population(population)
        # for NUM_GENERATIONS iterations
        for _1 in range(self.NUM_GENERATIONS):
            count += 1
            # print count
            # generate NUM_OFFSPRING children
            for _2 in range(self.NUM_OFFSPRING):
                population.append([self.crossover(self.select_parents(population)),0])
            # mutate and compute individual "fitness"
            population = self.mutate(population)
            population = self.evaluate_population(population)
        # sort population by decreasing fitness, select best individual
        self.cells = sorted(population, key=lambda x: x[1], reverse=True)[0][0]
        assert(len(self.cells) == self.numCells)
        self.cost = self.calc_cost(self.cells)
        # perform checks
        if self.reduce_congestion:
            for i,(x,y) in enumerate(self.cells.values()):
                weight = self.calc_weight(self.cells,x,y)
                assert weight <= self.width
        self.cost = self.calc_cost(self.cells)

    def select_parents(self, population):
        sorted_population = array([x[0] for x in sorted(population, key=lambda x: x[1], reverse=True)])
        ret = [choice(sorted_population[0:int(self.POP_SIZE/4)])]
        ret.append(choice(sorted_population))
        return ret

    def evaluate_population(self, population):
        """
            Two main goals in the "fitness" function for a given population:
            1. Ensure that circuits are sufficiently "pulled apart" to allow for routing resources between cells
            2. Ensure that routing resources are kept to a minimum (ie sum hp nets is minimized)

            Pulled-Apartness Cost = within bounding box, what is the average # of cells in each 2x2 cell grid
                - should approach 1 cell/box!
            Routing Resource Cost = sum of net half perimeters
                - normalize to 1
        """
        fitnesses = []
        for g,(genotype,_) in enumerate(population):
            F_nets = self.calc_cost(genotype)
            # print F_nets
            fitnesses.append((1/F_nets))

        max_b = 0
        # print "Fit best: " + str(1/max(fitnesses)) #+ ', worst: ' + str(1/min(fitnesses))
        for g,b in enumerate(fitnesses):
            if b > max_b:
                max_b = b
        for g,b in enumerate(fitnesses):
            b = b/max_b
            population[g][1] = b
        # print [x[1] for x in sorted(population, key=lambda x: x[1], reverse=True)[0:self.POP_SIZE]]
        return sorted(population, key=lambda x: x[1], reverse=True)[0:self.POP_SIZE]


    def calc_cost(self, genotype):
        """
        """
        cost = 0
        for i, net in enumerate(self.nets):
            cost += self.calc_half_perimeter(net, genotype)
        return cost


    def calc_half_perimeter(self, net, genotype):
        """
        """
        deltax = 0
        deltay = 0
        [source, sinks] = net
        for sink in sinks:
            assert genotype[sink][0] in range(self.nx) and genotype[sink][1] in range(self.ny)
            dx = abs(genotype[source][0] - genotype[sink][0])
            if dx > deltax:
                deltax = dx
            dy = abs(genotype[source][1] - genotype[sink][1])
            if dy > deltay:
                deltay = dy
        return deltax + deltay

    def generate_individual(self):
        """
        """
        genotype = {}
        for i in range(self.numCells):
            x = choice(range(self.nx))
            y = choice(range(self.ny))
            if self.reduce_congestion:
                weight = self.calc_weight(genotype,x,y)
            else:
                weight = 0
            while (x,y) in genotype.values() or weight >= self.width:
                x = choice(range(self.nx))
                y = choice(range(self.ny))
                if self.reduce_congestion:
                    weight = self.calc_weight(genotype,x,y)
                else:
                    weight = 0
            genotype[i] = (x,y)
        return genotype

    def crossover(self, parents):
        """

        """
        random.shuffle(parents)
        [parent1, parent2] = parents
        genotype = {}
        for i in range(self.numCells):
            (x, y) = parent1[i]
            if self.reduce_congestion:
                weight = self.calc_weight(genotype,x,y)
            else:
                weight = 0
            if (x,y) in list(genotype.values()) or weight >= self.width:
                (x, y) = parent2[i]
                if self.reduce_congestion:
                    weight = self.calc_weight(genotype,x,y)
                else:
                    weight = 0
            # if full, put in "nearby" cell - injects some randomness
            while (x, y) in list(genotype.values()) or weight >= self.width:
                x = choice(range(self.nx))
                y = choice(range(self.ny))
                if self.reduce_congestion:
                    weight = self.calc_weight(genotype,x,y)
                else:
                    weight = 0
            genotype[i] = (x, y)
            if self.reduce_congestion:
                for (x,y) in genotype.values():
                    weight = self.calc_weight(genotype,x,y)
                    assert weight <= self.width
        return genotype

    def mutate(self, population):
        """
            randomly select cells. ~ 1/5 of population
            randomly select a cell and another position x,y, exchange cells
        """
        for _1 in range(int(len(population) / 5)):
            i = choice(range(len(population)))
            genotype = population[i][0]
            for _2 in range(1):
                cell = choice(list(genotype.keys()))
                (x,y) = (choice(range(self.nx)), choice(range(self.ny)))
                if self.reduce_congestion:
                    weight = self.calc_weight(genotype,x,y)
                else:
                    weight = 0
                while (x, y) in genotype.values() or weight >= self.width:
                    (x, y) = (choice(range(self.nx)), choice(range(self.ny)))
                    if self.reduce_congestion:
                        weight = self.calc_weight(genotype,x,y)
                    else:
                        weight = 0
                genotype[cell] = (x,y)
                population[i][0] = genotype
                if self.reduce_congestion:
                    for (x,y) in genotype.values():
                        weight = self.calc_weight(genotype,x,y)
                        assert weight <= self.width

        return population

    def calc_weight(self,genotype,x,y):
        weight = 0
        _x = x
        _y = y
        if self.width <= 2:
            if x % 2:
                _x = x-1
            if y % 2:
                _y = y-1
            if (_x,_y) in genotype.values():
                weight += 1
            if (_x+1,_y) in genotype.values():
                weight += 1
            if (_x,_y+1) in genotype.values():
                weight += 1
            if (_x+1,_y+1) in genotype.values():
                weight += 1
        else:
            _x = _x - (x%4)
            _y = _y - (y%4)
            xvals = [_x,_x+2,_x,_x+2]
            yvals = [_y,_y,_y+2,_y+2]
            for i in range(4):
                if (xvals[i],yvals[i]) in genotype.values():
                    weight += 1
                if (xvals[i]+1,yvals[i]) in genotype.values():
                    weight += 1
                if (xvals[i],yvals[i]+1) in genotype.values():
                    weight += 1
                if (xvals[i]+1,yvals[i]+1) in genotype.values():
                    weight += 1
            weight = weight/4
        return weight

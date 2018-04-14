import random
class Grid:
    def __init__(self,f):
        # self.count = 0

        line = f.readline().split()
        # print line

        [self.xmax, self.ymax] = [int(s) for s in line]

        self.cells = []

        self.grid = []
        for y in range(self.ymax):
            row = []
            for x in range(self.xmax):
                row.append(Point(x,y))
            self.grid.append(row)

        self.walls = []
        for _ in range(int(f.readline().split()[0])):
            pass
            # [x, y] = [int(s) for s in f.readline().split()]
            # self.updatestatus(Point(x, y), 'wall')
            # self.walls.append(Point(x, y))

        self.inputs = []
        for _ in range(int(f.readline().split()[0])):
            line = [int(s) for s in f.readline().split()]
            for i in range(line[0]):
                if [line[2*i+1],line[2*i+2]] not in self.cells:
                    self.cells.append([line[2*i+1],line[2*i+2]])
                self.addweight(Point(line[2*i+1],line[2*i+2]))
                self.inputs.append([Point(line[2*i+1],line[2*i+2]),-1])
        
        self.outputs = []
        for _ in range(int(f.readline().split()[0])):
            line = [int(s) for s in f.readline().split()]
            assert line[0] == 1
            if [line[1],line[2]] not in self.cells:
                self.cells.append([line[1],line[2]])
            self.addweight(Point(line[1],line[2]))
            self.outputs.append([Point(line[1],line[2]),-1])

        self.routes = []
        for num in range(int(f.readline().split()[0])):
            new_wire = f.readline().split()
            source = [Point(int(new_wire[1]), int(new_wire[2])),-1]
            self.addweight(Point(int(new_wire[1]), int(new_wire[2])))
            if [int(new_wire[1]), int(new_wire[2])] not in self.cells:
                self.cells.append([int(new_wire[1]), int(new_wire[2])])
            sinks = []
            for i in range(int(new_wire[0]) - 1):
                if [int(new_wire[3 + 2 * i]), int(new_wire[4 + 2 * i])] not in self.cells:
                    self.cells.append([int(new_wire[3 + 2 * i]), int(new_wire[4 + 2 * i])])
                sinks.append([Point(int(new_wire[3 + 2 * i]), int(new_wire[4 + 2 * i])),-1])
                self.addweight(Point(int(new_wire[3 + 2 * i]), int(new_wire[4 + 2 * i])))
            self.addroute(source, sinks)

        self.sols = []
        self.failed_routes = []

    def iterativeRefineRoute(self):
        # inputs, outputs first so that we don't run out of space for them
        for cell in self.inputs:
            pt = self.getpt(cell[0])
            to_pick = []
            for i in range(4):
                if pt.qubits[i] == ' ':
                    to_pick.append(i)
            random.shuffle(to_pick)
            cell[1] = to_pick[0]
            pt.qubits[to_pick[0]] = 'wall'

        for cell in self.outputs:
            pt = self.getpt(cell[0])
            to_pick = []
            for i in range(4):
                if pt.qubits[i] == ' ':
                    to_pick.append(i)
            random.shuffle(to_pick)
            cell[1] = to_pick[0]
            pt.qubits[to_pick[0]] = 'wall'
        #######

        temp_sols = []
        routes = []
        for [source,sinks] in self.routes:
            routes.append([source,sinks])
        random.shuffle(routes)
        # for num,[source, sinks] in enumerate(routes):
        while len(routes) > 0:
            [source,sinks] = routes[0]
            # keep track of number sinks that can use a q-bit channel
            matches = [0,0,0,0]
            # keep track of which channels can be used by source
            valid = [False, False, False, False]
            # track which cells don't work with refined placement
            mismatches = [[],[],[],[]]
            for q in range(4):
                if source[0].qubits[q] != 'wall':
                    # True if nothing is placed there yet
                    valid[q] = True
            for q in range(4):
                if valid[q]:
                    for n,sink in enumerate(sinks):
                        if sink[0].qubits[q] != 'wall':
                            matches[q] = matches[q] + 1
                        else:
                            # can't put current sink in the desired channel. Add to mismatches to look at later
                            mismatches[q].append(n)
            # find channel(s) with most matches, pick one with "least routing" aka smallest hp sum
            to_pick = []
            for n,val in enumerate(matches):
                if val == max(matches):
                    to_pick.append(n)
            # iterate through valid values and pick one randomly
            # idx now contains primary net index
            random.shuffle(to_pick)
            idx = to_pick[0]
            source[1] = idx
            source[0].qubits[idx] = 'wall'
            # look at cells that fail this placement
            for n in mismatches[idx]:
                sink = sinks[n]
                to_pick = []
                for q in range(4):
                    if sink[0].qubits[q] != 'wall':
                        to_pick.append(q)
                # pick random empty cell
                random.shuffle(to_pick)
                sink[1] = to_pick[0]
                sink[0].qubits[to_pick[0]] = 'wall'
            for sink in sinks:
                if sink[1] == -1:
                    sink[1] = idx
                    sink[0].qubits[idx] = 'wall'

            # we now have source, sinks for all of these. Try routing.
            sols = []
            for sink in sinks:
                self.updatestatus(sink,'trace')
            # solve once for each source, sink pair
            random.shuffle(sinks)
            for sinknum,sink in enumerate(sinks):
                retry = True
                tried = []
                while (retry):
                    self.updatestatus(source,'trace')
                    sol = []
                    ## Initiate FIFO by adding source location
                    self.setdistance(source,1)
                    fifo = [source]
                    done = False
                    ## continue iterating over the next available points
                    ## while they are present in the FIFO and we have not
                    ## encountered the goal sink
                    while (fifo != []) and not done:
                        # current location is first in FIFO
                        current = fifo[0]
                        # peek at neighbouring values
                        next = self.walk(current)
                        # also add empty points in current cell
                        for q in range(4):
                            if q != current[1]:
                                if self.getpt(current[0]).qubits[q] is not 'wall':
                                    next.append([current[0],q])
                        # for each neighbouring value, compare to goal sink
                        # if they match, finish execution
                        for point in next:
                            if point[0].match(sink[0]) and not done and (point[1] == sink[1]):
                                done = True
                                self.setdistance(point,self.getpt(current[0]).distance[current[1]]+1)
                        # for each valid neighbouring value, increment distance
                        # and append to FIFO\
                        if not done:
                            for point in next:
                                if self.getpt(point[0]).distance[point[1]] == 0:
                                    fifo.append(point)
                                    self.setdistance(point, self.getpt(current[0]).distance[current[1]]+1)
                        # remove current point from FIFO
                        fifo.pop(0)
                    ## done finding solution to sink, if it exists
                    # print str(source[1])+' '+str(source[0].x)+' '+str(source[0].y) +' to ' + str(sink[1])+' '+str(sink[0].x)+' '+str(sink[0].y)
                    # self.printdist()
                    if done:
                        # initiate current location with sink
                        current = sink
                        sol = [sink]
                        # compare current location with source
                        while not current[0].match(source[0]):
                            # iterate over neighbouring values. If one has a
                            # distance = current distance-1, append it to the
                            # current solution and update current location
                            next = self.walk(current)
                            for qbit in range(4):
                                if qbit != current[1]:
                                    if self.getpt(current[0]).qubits[qbit] is not 'wall':
                                        next.append([current[0],qbit])
                            random.shuffle(next)
                            for point in next:
                                if self.getpt(point[0]).distance[point[1]] == self.getpt(current[0]).distance[current[1]]-1:
                                    if not point[0].match(source[0]):
                                        sol.append(point)
                                    current = point
                                    break
                        sol.append(source)
                        # finish solution
                        for point in sol:
                            self.updatestatus(point,'trace')
                        sols.append(sol)
                        retry = False
                    else:
                        # print "fail from " + str(source[0].x) + ' ' + str(source[0].y) + " " + str(sink[0].x) + ' ' + str(sink[0].y)
                        # do a rip-up and re-route, only fail if the sink can't go anywhere else
                        fail = True
                        tried.append(sink[1])
                        for q in range(4):
                            if q != sink[1] and q not in tried and self.getpt(sink[0]).qubits[q] is not 'wall':
                                # another valid option, change to this
                                self.getpt(sink[0]).qubits[sink[1]] = ' '
                                sink[1] = q
                                self.getpt(sink[0]).qubits[sink[1]] = 'trace'
                                fail = False
                                break
                        if fail:
                            # print "failed " + str(source[0].x) + ' ' + str(source[0].y)
                            retry = False
                            # add points to list of fails
                            self.failed_routes.append([source,sink])

                    self.cleardistance()

            self.updatestatus(source, 'wall')
            for sink in sinks:
                self.updatestatus(sink, 'wall')
            for sol in sols:
                for point in sol:
                    self.updatestatus(point,'wall')
            if len(sols) > 0:
                temp_sols.append(sols)
            routes.pop(0)
            ####### END ROUTING
        for each in temp_sols:
            for sol in each:
                self.sols.append(sol)

    # def refinePlacement(self):
    #     # keep track of net sizes on each qbit channel so that we can try to balance between them
    #     weights = [0,0,0,0]
    #     routes = []
    #     for [source,sinks] in self.routes:
    #         routes.append([source,sinks])
    #     random.shuffle(routes)
    #     for num,[source, sinks] in enumerate(routes):
    #         # print "net "+str(num+1)+"/"+str(len(self.routes))
    #         ptlist = [self.getpt(source[0])]
    #         qbitlist = [source[1]]
    #         assert source[1] == -1
    #         for sink in sinks:
    #             ptlist.append(self.getpt(sink[0]))
    #             qbitlist.append(sink[1])
    #             assert sink[1] == -1
    #         matches = [0,0,0,0]
    #         mismatches = [[],[],[],[]]
    #         for qbit_idx in range(4):
    #             for i,pt in enumerate(ptlist):
    #                 if pt.qubits[qbit_idx] == ' ':
    #                     matches[qbit_idx] = matches[qbit_idx] + 1
    #                 else:
    #                     mismatches[qbit_idx].append(i)
    #         to_pick = []
    #         for n,each in enumerate(matches):
    #             if each == max(matches):
    #                 to_pick.append(n)
    #         idx = to_pick[0]
    #         cw = weights[0]
    #         for index in to_pick:
    #             if weights[index] < cw:
    #                 cw = weights[index]
    #                 idx = index

    #         for i in mismatches[idx]:
    #             for qbit_idx in range(4):
    #                 if ptlist[i].qubits[qbit_idx] == ' ':
    #                     ptlist[i].qubits[qbit_idx] = 'wall'
    #                     if i==0:
    #                         source[1] = qbit_idx
    #                     else:
    #                         sinks[i-1][1] = qbit_idx
    #                     break

    #         for pt in ptlist:
    #             if self.getpt(pt).qubits[idx] == ' ':
    #                 self.getpt(pt).qubits[idx] = 'wall'
    #         if source[1] == -1:
    #             source[1] = idx
    #         for sink in sinks:
    #             if sink[1] == -1:
    #                 sink[1] = idx

    #         # add half perimeter of net to the weight
    #         for sink in sinks:
    #             if sink[1] == source[1]:
    #                 weights[idx] = weights[idx] + abs(sink[0].x - source[0].x) + abs(sink[0].y - source[0].y)
    #     # inputs, outputs
    #     for cell in self.inputs:
    #         pt = self.getpt(cell[0])
    #         # print pt.qubits
    #         for i in range(4):
    #             if pt.qubits[i] == ' ':
    #                 cell[1] = i 
    #                 pt.qubits[i] = 'wall'
    #                 break
    #     for cell in self.outputs:
    #         pt = self.getpt(cell[0])
    #         # print pt.qubits
    #         for i in range(4):
    #             if pt.qubits[i] == ' ':
    #                 cell[1] = i 
    #                 pt.qubits[i] = 'wall'
    #                 break
    #     # print weights

    # def LeeMoore(self):
    #     self.refinePlacement()
    #     routes = []
    #     for [source,sinks] in self.routes:
    #         routes.append([source,sinks])
    #     random.shuffle(routes)
    #     for [source,sinks] in routes:
    #         sols = []
    #         for sink in sinks:
    #             self.updatestatus(sink,'trace')
    #         # solve once for each source, sink pair
    #         for sink in sinks:
    #             # if (sink[1] == source[1]):
    #             self.updatestatus(source,'trace')
    #             sol = []
    #             ## Initiate FIFO by adding source location
    #             self.setdistance(source,1)
    #             fifo = [source]
    #             done = False
    #             ## continue iterating over the next available points
    #             ## while they are present in the FIFO and we have not
    #             ## encountered the goal sink
    #             while (fifo != []) and not done:
    #                 # current location is first in FIFO
    #                 current = fifo[0]
    #                 # peek at neighbouring values
    #                 next = self.walk(current)
    #                 # also add empty points in current cell
    #                 for qbit in range(4):
    #                     if qbit != current[1]:
    #                         if self.getpt(current[0]).qubits[qbit] is not 'wall':
    #                             next.append([current[0],qbit])
    #                 # random.shuffle(next)
    #                 # for each neighbouring value, compare to goal sink
    #                 # if they match, finish execution
    #                 for point in next:
    #                     if point[0].match(sink[0]) and not done and (point[1] == sink[1]):
    #                         done = True
    #                         self.setdistance(point,self.getpt(current[0]).distance[current[1]]+1)
    #                 # for each valid neighbouring value, increment distance
    #                 # and append to FIFO\
    #                 if not done:
    #                     for point in next:
    #                         if self.getpt(point[0]).distance[point[1]] == 0:
    #                             fifo.append(point)
    #                             self.setdistance(point,self.getpt(current[0]).distance[current[1]]+1)
    #                 # remove current point from FIFO
    #                 fifo.pop(0)
    #             ## done finding solution to sink, if it exists
    #             # print str(source[1])+' '+str(source[0].x)+' '+str(source[0].y) +' to ' + str(sink[1])+' '+str(sink[0].x)+' '+str(sink[0].y)
    #             # self.printdist()
    #             if done:
    #                 # initiate current location with sink
    #                 current = sink
    #                 sol = [sink]
    #                 # compare current location with source
    #                 while not current[0].match(source[0]):
    #                     # iterate over neighbouring values. If one has a
    #                     # distance = current distance-1, append it to the
    #                     # current solution and update current location
    #                     next = self.walk(current)
    #                     for qbit in range(4):
    #                         if qbit != current[1]:
    #                             if self.getpt(current[0]).qubits[qbit] is not 'wall':
    #                                 next.append([current[0],qbit])
    #                     random.shuffle(next)
    #                     for point in next:
    #                         if self.getpt(point[0]).distance[point[1]] == self.getpt(current[0]).distance[current[1]]-1:
    #                             if not point[0].match(source[0]):
    #                                 sol.append(point)
    #                             current = point
    #                             break
    #                 sol.append(source)
    #                 # finish solution
    #                 for point in sol:
    #                     self.updatestatus(point,'trace')
    #                 sols.append(sol)
    #             # else:
    #                 # print "fail from " + str(source[0].x) + ' ' + str(source[0].y) + " " + str(sink[0].x) + ' ' + str(sink[0].y)
    #             self.cleardistance()
    #             # else:
    #             #     print "mismatch"

    #         self.updatestatus(source, 'wall')
    #         for sink in sinks:
    #             self.updatestatus(sink, 'wall')
    #         for sol in sols:
    #             for point in sol:
    #                 self.updatestatus(point,'wall')
    #             self.sols.append(sol)

    def walk(self, point):
        pt = point[0]
        i = point[1]
        if not pt:
            return []
        else:
            return [[s,i] for s in [self.above(point),self.below(point),self.right(point),self.left(point)] if s is not None and s.qubits[i] is not 'wall']

    # def probe(self, point, vertical, increment, sinks):
    #     pt = point[0]
    #     i = point[1]
    #     if not pt:
    #         return False
    #     else:
    #         for new in self.walk(point):
    #             for each in sinks:
    #                 if new[0].match(each[0]):
    #                     return each
    #         newpt = self.getpt(Point(pt.x if vertical else pt.x+1 if increment else pt.x-1,
    #                                 pt.y if not vertical else pt.y + 1 if increment else pt.y - 1))
    #         if newpt is not None:
    #             return [newpt,i] if newpt.qubits[i] != 'wall' else False
    #         else:
    #             return False

    # def printgrid(self):
    #     for y in range(self.ymax):
    #         line = ""
    #         for x in range(self.xmax):
    #             line += str(self.grid[y][x].weight)
    #         print line

    def printdist(self):
        for q in range(4):
            print q
            for y in range(self.ymax):
                line = ""
                for x in range(self.xmax):
                    line += "%02d"%(self.grid[y][x].distance[q])+' '
                print line

    def getpt(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x]
        else:
            return None

    # def status(self,point):
    #     pt = point[0]
    #     i = point[1]
    #     if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
    #         return self.grid[pt.y][pt.x].qubits[i]
    #     else:
    #         return False

    def above(self,pt):
        if (pt[0].x in range(self.xmax)) & (pt[0].y+1 in range(self.ymax)):
            return self.grid[pt[0].y+1][pt[0].x]
        else:
            return None

    def below(self,pt):
        if (pt[0].x in range(self.xmax)) & (pt[0].y-1 in range(self.ymax)):
            return self.grid[pt[0].y-1][pt[0].x]
        else:
            return None

    def right(self,pt):
        if (pt[0].x+1 in range(self.xmax)) & (pt[0].y in range(self.ymax)):
            return self.grid[pt[0].y][pt[0].x+1]
        else:
            return None

    def left(self,pt):
        if (pt[0].x-1 in range(self.xmax)) & (pt[0].y in range(self.ymax)):
            return self.grid[pt[0].y][pt[0].x-1]
        else:
            return None

    def addweight(self,pt):
        if (pt.x in range(self.xmax)) and (pt.y in range(self.ymax)):
            assert self.getpt(pt).weight <= 3
            self.getpt(pt).weight = self.getpt(pt).weight + 1

    def updatestatus(self,point,ptype):
        pt = point[0]
        i = point[1]
        if (pt.x in range(self.xmax)) and (pt.y in range(self.ymax)):
            if ptype in ['wall']:
                self.getpt(pt).qubits[i] = 'wall'
            elif ptype in ['clear']:
                self.grid[pt.y][pt.x].qubits[i] = ' '
            elif ptype in ['trace']:
                self.grid[pt.y][pt.x].qubits[i] = 'x'
            elif int(ptype)>0: #ie '1' '2'
                self.grid[pt.y][pt.x].qubits[i] = ptype
            else:
                return False
        else:
            return False
        return True

    def addroute(self,source,sinks):
        if (source[0].x not in range(self.xmax)) or (source[0].y not in range(self.ymax)):
            return False
        for sink in sinks:
            if (sink[0].x not in range(self.xmax)) or (sink[0].y not in range(self.ymax)):
                return False
        self.routes.append([source,sinks])
        return True

    def setdistance(self,pt,d):
        if (pt[0].x in range(self.xmax)) & (pt[0].y in range(self.ymax)):
            self.getpt(pt[0]).distance[pt[1]] = d
            return True
        else:
            return False

    def cleardistance(self):
        for y in range(self.ymax):
            for x in range(self.xmax):
                for q in range(4):
                    self.grid[y][x].distance[q] = 0


class Point:
    # a single x,y point in the circuit grid
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.qubits = [' ',' ',' ',' ']
        self.distance = [0,0,0,0]
        self.weight = 0

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def match(self,pt):
        if (pt.x == self.x) and (pt.y == self.y):
            return True
        else:
            return False

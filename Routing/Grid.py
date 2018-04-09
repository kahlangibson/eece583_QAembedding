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

        self.refinePlacement()

        self.sols = []

    def refinePlacement(self):
        for num,[source, sinks] in enumerate(self.routes):
            # print "net "+str(num+1)+"/"+str(len(self.routes))
            ptlist = [self.getpt(source[0])]
            qbitlist = [source[1]]
            assert source[1] == -1
            for sink in sinks:
                ptlist.append(self.getpt(sink[0]))
                qbitlist.append(sink[1])
                assert sink[1] == -1
            matches = [0,0,0,0]
            mismatches = [[],[],[],[]]
            for qbit_idx in range(4):
                for i,pt in enumerate(ptlist):
                    if pt.qubits[qbit_idx] == ' ':
                        matches[qbit_idx] = matches[qbit_idx] + 1
                    else:
                        mismatches[qbit_idx].append(i)
            to_pick = []
            for n,each in enumerate(matches):
                if each == max(matches):
                    to_pick.append(n)
            idx = random.choice(to_pick)
            # print " mismatches: "+str(len(mismatches[idx]))+"/"+str(len(ptlist))
            for i in mismatches[idx]:
                for qbit_idx in range(4):
                    if ptlist[i].qubits[qbit_idx] == ' ':
                        ptlist[i].qubits[qbit_idx] = 'wall'
                        if (i==0):
                            source[1] = qbit_idx
                        else:
                            sinks[i-1][1] = qbit_idx
                        break
            for pt in ptlist:
                if self.getpt(pt).qubits[idx] == ' ':
                    self.getpt(pt).qubits[idx] = 'wall'
            if source[1] == -1:
                source[1] = idx
            for sink in sinks:
                if sink[1] == -1:
                    sink[1] = idx
        # inputs, outputs
        for cell in self.inputs:
            pt = self.getpt(cell[0])
            # print pt.qubits
            for i in range(4):
                if pt.qubits[i] == ' ':
                    cell[1] = i 
                    pt.qubits[i] = 'wall'
                    break
        for cell in self.outputs:
            pt = self.getpt(cell[0])
            # print pt.qubits
            for i in range(4):
                if pt.qubits[i] == ' ':
                    cell[1] = i 
                    pt.qubits[i] = 'wall'
                    break

    def walk(self, point):
        pt = point[0]
        i = point[1]
        if not pt:
            return []
        else:
            return [[s,i] for s in [self.above(point),self.below(point),self.right(point),self.left(point)] if s is not None and s.qubits[i] is not 'wall']

    def probe(self, point, vertical, increment, sinks):
        pt = point[0]
        i = point[1]
        if not pt:
            return False
        else:
            for new in self.walk(point):
                for each in sinks:
                    if new[0].match(each[0]):
                        return each
            newpt = self.getpt(Point(pt.x if vertical else pt.x+1 if increment else pt.x-1,
                                    pt.y if not vertical else pt.y + 1 if increment else pt.y - 1))
            if newpt is not None:
                return [newpt,i] if newpt.qubits[i] != 'wall' else False
            else:
                return False


    def printgrid(self):
        for y in range(self.ymax):
            line = ""
            for x in range(self.xmax):
                line += str(self.grid[y][x].weight)
            print line

    def printdist(self):
        for y in range(self.ymax):
            line = ""
            for x in range(self.xmax):
                line += str(self.grid[y][x].distance)+' '
            print line

    def getpt(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x]
        else:
            return None

    def status(self,point):
        pt = point[0]
        i = point[1]
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x].qubits[i]
        else:
            return False

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

    # def addwall(self,wall):
    #     if (wall.x not in range(self.xmax)) or (wall.y not in range(self.ymax)):
    #         return False
    #     self.walls.append(wall)
    #     return True

    def setdistance(self,pt,d):
        if (pt[0].x in range(self.xmax)) & (pt[0].y in range(self.ymax)):
            self.getpt(pt[0]).distance = d
            return True
        else:
            return False

    def cleardistance(self):
        for y in range(self.ymax):
            for x in range(self.xmax):
                self.grid[y][x].distance = 0

    def LeeMoore(self):
        routes = []
        for [source,sinks] in self.routes:
            routes.append([source,sinks])
        for [source,sinks] in routes:
            sols = []
            for sink in sinks:
                self.updatestatus(sink,'trace')
            # solve once for each source, sink pair
            for sink in sinks:
                if (sink[1] == source[1]):
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
                        # for each neighbouring value, compare to goal sink
                        # if they match, finish execution
                        for point in next:
                            if point[0].match(sink[0]) and not done and (point[1] == sink[1]):
                                done = True
                                self.setdistance(point,self.getpt(current[0]).distance+1)
                        # for each valid neighbouring value, increment distance
                        # and append to FIFO
                        # TODO also append in 3-d directions whenever there are other choices
                        if not done:
                            for point in next:
                                if self.getpt(point[0]).distance == 0:
                                    fifo.append(point)
                                    self.setdistance(point,self.getpt(current[0]).distance+1)
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
                            for point in next:
                                if self.getpt(point[0]).distance == self.getpt(current[0]).distance-1:
                                    if not point[0].match(source[0]):
                                        sol.append(point)
                                    current = point
                                    break
                        sol.append(source)
                        # finish solution
                        for point in sol:
                            self.updatestatus(point,'trace')
                        sols.append(sol)
                    else:
                        print "fail"
                    self.cleardistance()
                else:
                    print "mismatch"

            self.updatestatus(source, 'wall')
            for sink in sinks:
                self.updatestatus(sink, 'wall')
            for sol in sols:
                for point in sol:
                    self.updatestatus(point,'wall')
                self.sols.append(sol)

class Point:
    # a single x,y point in the circuit grid
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.qubits = [' ',' ',' ',' ']
        self.distance = 0
        self.weight = 0

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def match(self,pt):
        if (pt.x == self.x) and (pt.y == self.y):
            return True
        else:
            return False

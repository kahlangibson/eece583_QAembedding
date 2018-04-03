class Grid:
    # a map representing the input graph and properties of the infile
    # once instantiated, this class will populate the objects, sources, and
    # sinks provided by the infile. Calling the methods grid.LeeMoore or
    # grid.LineProbe will populate the solution list based on the provided information
    def __init__(self,f):
        self.count = 0

        [self.xmax, self.ymax] = [int(s) for s in f.readline().split()]

        self.grid = []
        for y in range(self.ymax):
            row = []
            for x in range(self.xmax):
                row.append(Point(x,y))
            self.grid.append(row)

        self.walls = []
        for _ in range(int(f.readline().split()[0])):
            [x, y] = [int(s) for s in f.readline().split()]
            self.updatestatus(Point(x, y), 'wall')
            self.walls.append(Point(x, y))

        self.routes = []
        for num in range(int(f.readline().split()[0])):
            new_wire = f.readline().split()
            source = Point(int(new_wire[1]), int(new_wire[2]))
            self.updatestatus(source, 'wall')

            sinks = []
            for i in range(int(new_wire[0]) - 1):
                sinks.append(Point(int(new_wire[3 + 2 * i]), int(new_wire[4 + 2 * i])))
                self.updatestatus(Point(int(new_wire[3 + 2 * i]), int(new_wire[4 + 2 * i])), 'wall')

            self.addroute(source, sinks)

        for _,(s,si) in enumerate(self.routes):
            for each in si:
                self.count += 1

        self.sols = []

    def walk(self, pt):
        if not pt:
            return []
        else:
            return [s for s in [self.above(pt),self.below(pt),self.right(pt),self.left(pt)] if s is not None and s.status is not '0']

    def probe(self, pt, vertical, increment, sinks):
        if not pt:
            return False
        else:
            for point in self.walk(pt):
                for each in sinks:
                    if point.match(each):
                        return each

            newpt = self.getpt(Point(pt.x if vertical else pt.x+1 if increment else pt.x-1,
                                    pt.y if not vertical else pt.y + 1 if increment else pt.y - 1))

            if newpt is not None:
                return newpt if newpt.status != '0' else False
            else:
                return False


    def printgrid(self):
        for y in range(self.ymax):
            line = ""
            for x in range(self.xmax):
                line += str(self.grid[y][x].status)
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

    def status(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x].status
        else:
            return False

    def above(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y+1 in range(self.ymax)):
            return self.grid[pt.y+1][pt.x]
        else:
            return None

    def below(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y-1 in range(self.ymax)):
            return self.grid[pt.y-1][pt.x]
        else:
            return None

    def right(self,pt):
        if (pt.x+1 in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x+1]
        else:
            return None

    def left(self,pt):
        if (pt.x-1 in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x-1]
        else:
            return None

    def updatestatus(self,pt,ptype):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            if ptype in ['wall']:
                self.getpt(pt).status = '0'
            elif ptype in ['clear']:
                self.grid[pt.y][pt.x].status = ' '
            elif ptype in ['trace']:
                self.grid[pt.y][pt.x].status = 'x'
            elif int(ptype)>0: #ie '1' '2'
                self.grid[pt.y][pt.x].status = ptype
            else:
                return False
        else:
            return False
        return True

    def addroute(self,source,sinks):
        if (source.x not in range(self.xmax)) or (source.y not in range(self.ymax)):
            return False
        for sink in sinks:
            if (sink.x not in range(self.xmax)) or (source.y not in range(self.ymax)):
                return False
        self.routes.append([source,sinks])
        return True

    def addwall(self,wall):
        if (wall.x not in range(self.xmax)) or (wall.y not in range(self.ymax)):
            return False
        self.walls.append(wall)
        return True

    def setdistance(self,pt,d):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            self.getpt(pt).distance = d
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
                self.updatestatus(source,'trace')
                sol = []
                ## Initiate FIFO by adding source location
                self.setdistance(source,1)
                fifo = [self.getpt(source)]
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
                        if point.match(sink) and not done:
                            done = True
                            self.setdistance(point,current.distance+1)
                    # for each valid neighbouring value, increment distance
                    # and append to FIFO
                    if not done:
                        for point in next:
                            if point.distance == 0:
                                fifo.append(point)
                                self.setdistance(point,current.distance+1)
                    # remove current point from FIFO
                    fifo.pop(0)
                ## done finding solution to sink, if it exists
                if done:
                    # initiate current location with sink
                    current = self.getpt(sink)
                    # compare current location with source
                    while not current.match(self.getpt(source)):
                        # iterate over neighbouring values. If one has a
                        # distance = current distance-1, append it to the
                        # current solution and update current location
                        next = self.walk(current)
                        for point in next:
                            if point.distance == current.distance-1:
                                if not point.match(source):
                                    sol.append(point)
                                current = point
                    # finish solution
                    for point in sol:
                        self.updatestatus(point,'trace')
                    sols.append(sol)
                self.cleardistance()

            self.updatestatus(source, 'wall')
            for sink in sinks:
                self.updatestatus(sink, 'wall')
            for sol in sols:
                for point in sol:
                    self.updatestatus(point,'wall')
                self.sols.append(sol)

    def LineProbe(self):
        for num, [source, sinks] in enumerate(self.routes):
            print "Source " + str(num)
            sinks_todo = []
            for sink in sinks:
                self.updatestatus(sink, 'trace')
                sinks_todo.append(sink)
            self.updatestatus(source, 'trace')
            sols = []
            for i, sink in enumerate(sinks):
                print "Sink " + str(i)
                tempsol = []
                tempsol_count = 0 # only improve once!
                # if we have already solved for a sink, we can change starting point to be anywhere
                # along the trace
                start = source
                if sols != []:
                    for sol in sols:
                        for point in sol:
                            if (abs(point.x-sink.x) + abs(point.y-sink.y)) < (abs(start.x-sink.x) + abs(start.y-sink.y)):
                                start = point
                queue = [[start]]
                done = False

                while queue != [] and not done:
                    current = queue[0][-1]
                    bubbleroute = []
                    manx = sink.x - current.x
                    many = sink.y - current.y
                    queue_temp = False

                    queue_temp = []
                    if many != 0:
                        # check for possible movement in vertical direction
                        vertical = True
                        increment = (many > 0)
                        next = self.probe(current, vertical, increment, sinks_todo)
                        queue_temp.append(next)
                        queue_temp.append(self.probe(current, vertical, not increment, sinks_todo))
                    if manx != 0:
                        # check for possible movement in horizontal dir
                        # append other direction to queue if needed
                        vertical = False
                        increment = (manx > 0)
                        next = self.probe(current, vertical, increment, sinks_todo)
                        queue_temp.append(self.probe(current, vertical, not increment, sinks_todo))
                        for each in queue_temp:
                            if next and each and each.status != 'x':
                                if len(queue) < max(self.xmax,self.ymax):
                                    queue.append(queue[0]+[each])
                                else:
                                    if abs(len(queue[-1])-len(queue[0]+[each])) < max(self.xmax/4,self.ymax/4):
                                        queue.pop(1)
                                        queue.append(queue[0]+[each])
                    # else: maintain original next value, added nothing to queue

                    if next is not False:  # next move does not run us into a wall
                        if next.match(sink):
                            ## CASE 1: We have found the sink.
                            queue[0].append(next)
                            # check if current solution is better than one previously found,
                            # and if so, replace it. We have a counter to increment that prevents us
                            # from attempting to improve a solution too many times
                            if tempsol == [] or len(queue[0]) < len(tempsol):
                                if len(queue[0]) < len(tempsol): # an improvement
                                    tempsol_count += 1
                                tempsol = []
                                for point in queue[0]:
                                    tempsol.append(point)

                            # if we haven't reached the improvement limit and there are still objects in the queue,
                            # clear traces and restart with next queue object
                            if tempsol_count < 1 and len(queue) > 1: # more remain
                                for point in queue[0]:
                                    self.updatestatus(point, 'clear')
                                queue.pop(0)
                                for point in queue[0]:
                                    self.updatestatus(point,'trace')
                                self.updatestatus(source, 'trace')
                            # the saved solution is our best solution
                            else:
                                for n, each in enumerate(sinks_todo):
                                    if each.match(sink):
                                        sinks_todo.pop(n)
                                done = True
                                queue.pop(0)
                                sols.append([s for s in tempsol])

                        elif next.status != 'x':
                            # add new point! this point is a valid next move. Append to the solution
                            queue[0].append(next)
                            self.updatestatus(next, 'trace')
                        else:
                            # current point is not valid - but might be on our list of sinks. If it is a sink, append
                            # in order to reduce future routes to be made
                            flag = False
                            for point in sinks_todo:
                                if next.match(point):
                                    # successfully made an extra solution en route
                                    # pop from list of sinks to do
                                    # add point to list of sols
                                    for n,each in enumerate(sinks_todo):
                                        if each.match(next):
                                            sinks_todo.pop(n)
                                    queue[0].append(next)
                                    sols.append([point])
                                    self.updatestatus(next, 'trace')
                                    flag = True
                            # not a valid next move
                            if not flag:
                                # This route failed. Pop and move on"
                                for point in queue[0]:
                                    self.updatestatus(point,'clear')
                                queue.pop(0)
                                #  if the queue is empty, we are done. clear and add current best to list of solutions
                                #  if it exists
                                if queue != []:
                                    for point in queue[0]:
                                        self.updatestatus(point,'trace')
                                    self.updatestatus(source, 'trace')
                                elif tempsol != []:
                                    for n, each in enumerate(sinks_todo):
                                        if each.match(sink):
                                            sinks_todo.pop(n)
                                    done = True
                                    sols.append([s for s in tempsol])
                    else:  # we hit an obstacle, use Lee-Moore alteration to "bubble" around
                        # hit a wall. Create "bubble" paths until can continue in direction
                        fifo = [current]
                        current.distance = 1
                        flag = False
                        while (fifo != []) and not flag:
                            bubble = fifo[0]
                            nextpoint = self.probe(bubble, vertical, increment, sinks_todo)
                            # requirements for a valid Lee-Moore solution:
                            # 1: a point in the direction we would like to go exists
                            # 2. the next point is not a trace that we have already visited during line probe ('trace'=='x')
                            #       or that we have visited during Lee-Moore ('distance' != '0')
                            if nextpoint is not False and nextpoint.status != 'x' and self.getpt(
                                    nextpoint).distance == 0 and not flag:
                                flag = True
                                bubbleroute.append(bubble)
                            elif nextpoint is not False and nextpoint.match(sink):
                                flag = True
                                bubbleroute.append(bubble)
                            if not flag:
                                nextbubble = [each for each in self.walk(bubble) if each.status != 'x']
                                for point in nextbubble:
                                    if point.distance == 0:
                                        fifo.append(point)
                                        self.setdistance(point, bubble.distance + 1)
                            fifo.pop(0)
                        if flag:  # a solution was found
                            flag = False
                            while not flag:
                                walk = bubbleroute[-1]
                                backnext = self.walk(walk)
                                for point in backnext:
                                    if current.match(point):
                                        bubbleroute.append(point)
                                        flag = True
                                    elif point.distance == walk.distance-1 and not flag:
                                        bubbleroute.append(point)

                            # the bubbleroute solution is back to front - need to reverse
                            bubbleroute.reverse()
                            for point in bubbleroute:
                                queue[0].append(point)
                            # next point is the last point on the route
                            for point in bubbleroute:
                                self.updatestatus(point, 'trace')
                        else:  # no solution was found!
                            queue.pop(0)
                            if queue == [] and tempsol != []:
                                for n, each in enumerate(sinks_todo):
                                    if each.match(sink):
                                        sinks_todo.pop(n)
                                done = True
                                sols.append([s for s in tempsol])
                        self.cleardistance()

            for sol in sols:
                self.sols.append(sol)
                for point in sol:
                    self.updatestatus(point, 'wall')

            for x in range(self.xmax):
                for y in range(self.ymax):
                    if self.status(Point(x, y)) == 'x':
                        self.updatestatus(Point(x, y), 'clear')

            self.updatestatus(source, 'wall')
            for sink in sinks:
                self.updatestatus(sink, 'wall')


class Point:
    # a single x,y point in the circuit grid
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = ' '
        self.distance = 0

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def match(self,pt):
        if (pt.x == self.x) and (pt.y == self.y):
            return True
        else:
            return False

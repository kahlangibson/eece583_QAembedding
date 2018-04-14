from Grid import Grid
from os import listdir
from os.path import isfile, join

indir = "./Placing/output/"
outdir = "./Routing/output/"

files = [f for f in listdir(indir) if isfile(join(indir, f)) and '.txt' in f]
for file in files:
    compute = True
    count = 0
    print file
    while compute and count < 300:
        count += 1
        infile = open(join(indir,file))
        grid = Grid(infile)
        grid.iterativeRefineRoute()
        outfile = open(join(outdir,file), 'w')
        outfile.write(str(len(grid.cells))+'\n')
        for (x,y) in grid.cells:
            outfile.write(str(x)+' '+str(y)+'\n')
        outfile.write(str(len(grid.inputs))+'\n')
        for (cell,channel) in grid.inputs:
            outfile.write(str(channel)+' '+str(cell.x)+' '+str(cell.y)+'\n')
        outfile.write(str(len(grid.outputs))+'\n')
        for (cell,channel) in grid.outputs:
            outfile.write(str(channel)+' '+str(cell.x)+' '+str(cell.y)+'\n')
        outfile.write(str(len(grid.sols))+'\n')
        for sol in grid.sols:
            outfile.write(str(len(sol))+' ')
            for (cell,channel) in sol:
                outfile.write(str(channel)+' '+str(cell.x)+' '+str(cell.y) + ' ')
            outfile.write('\n')
        outfile.write(str(len(grid.failed_routes))+'\n')
        if len(grid.failed_routes) == 0:
            compute = False
        for [source,sink] in grid.failed_routes:
            outfile.write(str(source[0].x) + ' ' + str(source[0].y) + ' ' + str(source[1]) + ' ' + str(sink[0].x) + ' ' + str(sink[0].y) + ' ' + str(sink[1]) + '\n')
        outfile.close()

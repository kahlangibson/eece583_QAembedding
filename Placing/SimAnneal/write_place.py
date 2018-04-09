"""
write_place.py

Writes an output txt file describing the global placement result for input to routing

line 1: size of grid to use
line 2: number of obstructions/placed cells
TODO: this is oversimplified. a 2-in 1-out cell actually has the ability to route a wire through
TODO: add capability for determining utilized wire/cell weight
line 3+: x,y coordinates of obstructions
line 4: number of nets to route
line 5+: net data, formatted as <#pins source(x,y) sink_1(x,y) sink_2(x,y) ... sink_n(x,y)>

@:param circuit: circuit under test name string

lines 4-5 are pre-generated and passed as a list of strings
@:param nets:

@:param cells: list of cell x,y coordinates as tuples
"""
from os import listdir
from os.path import isfile, join

out_dir = "../output_simAnneal/"

def write_place(circuit, nets, cells, in_nets, out_nets):
    with open(out_dir+circuit, "w") as of:
        of.write("12 12\n")
        of.write(str(len(cells))+'\n')
        for cell in cells:
            of.write(str(cell[0])+' '+str(cell[1])+'\n')
        of.write(str(len(in_nets)) + '\n')
        for net in in_nets:
            line = str(len(net)) + ' '
            for n in net:
                line += str(n.x) + ' ' + str(n.y) + ' '
            line += '\n'
            of.write(line)
        of.write(str(len(out_nets)) + '\n')
        for net in out_nets:
            line = str(len(net)) + ' '
            for n in net:
                line += str(n.x) + ' ' + str(n.y) + ' '
            line += '\n'
            of.write(line)
        of.write(str(len(nets))+'\n')
        for net in nets:
            line = str(len(net))+' '
            for n in net:
                line += str(n.x)+' '+str(n.y)+' '
            line += '\n'
            of.write(line)
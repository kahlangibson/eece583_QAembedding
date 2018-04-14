from os import listdir
from os.path import isfile, join
from circuit import Circuit

dir = './Mapping/testnets/'
out_dir = './Placing/output/'

filenames = [f for f in listdir(dir) if isfile(join(dir, f)) and ".txt" in f]

def write_place(circuit, nets, cells, in_nets, out_nets):
    with open(out_dir + circuit, "w") as of:
        of.write("12 12\n")
        of.write(str(len(cells)) + '\n')
        for cell in cells:
            of.write(str(cell[0]) + ' ' + str(cell[1]) + '\n')
        of.write(str(len(in_nets)) + '\n')
        for net in in_nets:
            line = str(len(net)) + ' '
            for n in net:
                line += str(n[0]) + ' ' + str(n[1]) + ' '
            line += '\n'
            of.write(line)
        of.write(str(len(out_nets)) + '\n')
        for net in out_nets:
            line = str(len(net)) + ' '
            for n in net:
                line += str(n[0]) + ' ' + str(n[1]) + ' '
            line += '\n'
            of.write(line)
        of.write(str(len(nets)) + '\n')
        for net in nets:
            line = str(len(net)) + ' '
            for n in net:
                line += str(n[0]) + ' ' + str(n[1]) + ' '
            line += '\n'
            of.write(line)

for f in filenames:
    print f
    file = open(dir+f, 'r')
    c = Circuit(file)
    result = c.genetic()
    cells = []
    nets = []
    for [source,sinks] in c.nets:
        net = [c.cells[source]]
        for sink in sinks:
            net.append(c.cells[sink])
        nets.append(net)
    in_nets = []
    for input in c.inputs:
        net = []
        for each in input:
            net.append(c.cells[each])
        in_nets.append(net)
    out_nets = []
    for output in c.outputs:
        out_nets.append([c.cells[output[0]]])
    write_place(f, nets, cells, in_nets, out_nets)

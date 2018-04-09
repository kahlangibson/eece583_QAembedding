from os import listdir
from os.path import isfile, join
from draw import *
from write_place import write_place

dir = '../../Mapping/testnets/'

startT = 80.
beta = 0.6
exitRate = 0.25
runWith0 = True

def read_infile():
    global myCircuit
    runButton.pack_forget()
    if myCircuit is not None:
        myCircuit.delete()
    global filename
    filename = file.get()
    f = open(dir+filename, "r")  # gets closed inside simAnneal object
    myCircuit = draw(root, startT, beta, exitRate, runWith0, f)
    runButton.pack(side='left', padx=20, pady=10)

def runAnneal():
    global myCircuit
    myCircuit.runSimAnneal()
    cells = []
    # for cell in myCircuit.cells:
    #     cells.append([cell.x,cell.y])
    nets = []
    for [source,sinks] in myCircuit.nets:
        net = [myCircuit.cells[source]]
        for sink in sinks:
            net.append(myCircuit.cells[sink])
        nets.append(net)
    in_nets = []
    for input in myCircuit.inputs:
        net = []
        for each in input:
            net.append(myCircuit.cells[each])
        in_nets.append(net)
    out_nets = []
    for output in myCircuit.outputs:
        out_nets.append([myCircuit.cells[output[0]]])
    write_place(filename, nets, cells, in_nets, out_nets)


## main ##
root = Tk()
root.lift()
root.attributes("-topmost", True)
global runButton
runButton = tk.Button(root, text="Run Placement", command=runAnneal)

myCircuit = None

file = tk.StringVar(root)
# initial value
file.set('Choose File')
# filenames = [f for f in listdir('./benchmarks/') if isfile(join('./benchmarks/', f))]
filenames = [f for f in listdir(dir) if isfile(join(dir, f)) and ".txt" in f]
drop = tk.OptionMenu(root, file, *filenames)
drop.pack(side='left', padx=10, pady=10)
go = tk.Button(root, text="Choose File", command=read_infile)
go.pack(side='left', padx=20, pady=10)

root.mainloop()
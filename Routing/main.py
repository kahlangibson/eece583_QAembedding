from Tkinter import *
import Tkinter as tk
import Tkconstants, tkFileDialog
import Grid
from os import listdir
from os.path import isfile, join


class GridWindow:
    def __init__(self, parent):
        self.myParent = parent

        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)

        self.cellwidth = 0
        self.cellheight = 0
        self.rect = {}
        self.text = {}
        self.fails = 0

    def delete(self):
        self.myCanvas.delete('all')
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)

    def draw_grid(self, rows, columns):
        bigger = max(columns, rows)
        self.cellwidth = 1000/bigger
        self.cellheight = 1000/bigger

        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,
                                width=self.cellheight*rows,
                                height=self.cellwidth*columns)
        self.myCanvas.pack(side=tk.RIGHT)

        for column in range(rows):
            for row in range(columns):
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row, column] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def draw_walls(self, walls):
        for wall in walls:
            x1 = wall.x * self.cellwidth
            y1 = wall.y * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.rect[wall.x, wall.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="blue")

    def draw_routes(self, routes):
        colors = ["red", "yellow", "gray", "orange", "cyan", "pink", "green", "purple"]
        for num,[source,sinks] in enumerate(routes):
            x1 = source.x * self.cellwidth
            y1 = source.y * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.rect[source.x, source.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill=colors[num])
            self.text[source.x, source.y] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, text=num+1)
            for sink in sinks:
                x1 = sink.x * self.cellwidth
                y1 = sink.y * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[sink.x, sink.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill=colors[num])
                self.text[sink.x, sink.y] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, text=num+1)

    def draw_sols(self, sols):
        global counter
        sol = [sol for sol in sols if sol is not False][counter]
        for pt in sol:
            x1 = pt.x * self.cellwidth + self.cellwidth/4
            y1 = pt.y * self.cellheight + self.cellheight/4
            x2 = x1 + self.cellwidth/2
            y2 = y1 + self.cellheight/2
            self.rect[pt.x, pt.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill='black')
        print "done route " + str(counter)


def read_infile():
    global ggrid
    global lmbutton
    global lpbutton
    global counter_text
    myapp.delete()

    lmbutton.pack_forget()
    lpbutton.pack_forget()
    counter_text.pack_forget()

    filename = file.get()
    # f = open('./benchmarks/'+filename, "r")  # opens file with name of filename
    f = open('./benchmarks/'+filename, "r")

    myGrid = Grid.Grid(f)
    myapp.draw_grid(myGrid.xmax, myGrid.ymax)

    myapp.draw_walls(myGrid.walls)

    myapp.draw_routes(myGrid.routes)

    f.close()
    ggrid = myGrid


def route():
    global counter
    global ggrid
    global lmbutton
    global lpbutton
    global v
    counter = 0
    lmbutton.pack_forget()
    lpbutton.pack_forget()
    v.set('')
    if var.get() == 'Lee Moore':
        if ggrid.sols != []:
            read_infile()
        ggrid.LeeMoore()
        counter = 0
        lmbutton.pack(side='left', padx=20, pady=10)
        root.mainloop()
    if var.get() == 'Line Probe':
        if ggrid.sols != []:
            read_infile()
        ggrid.LineProbe()
        counter = 0
        lpbutton.pack(side='left', padx=20, pady=10)
        root.mainloop()

def inc_counter_lm():
    global counter
    global ggrid
    global lmbutton
    global v
    if counter < len(ggrid.sols):
        myapp.draw_sols(ggrid.sols)
        counter += 1
        if counter == len(ggrid.sols):
            lmbutton.pack_forget()
            v.set(str(len(ggrid.sols))+"/"+str(ggrid.count)+" sinks")
            counter_text.pack(side='left', padx=20, pady=10)


def inc_counter_lp():
    global counter
    global ggrid
    global lpbutton
    global v
    if counter < len(ggrid.sols):
        myapp.draw_sols(ggrid.sols)
        counter += 1
        if counter == len(ggrid.sols):
            lpbutton.pack_forget()
            v.set(str(len(ggrid.sols))+"/"+str(ggrid.count)+" sinks")
            counter_text.pack(side='left', padx=20, pady=10)
    pass

## main ##
root = Tk()
root.lift()
root.attributes("-topmost", True)

myapp = GridWindow(root)

global lmbutton
global lpbutton
global counter_text
global v
v = tk.StringVar()
lmbutton = tk.Button(root, text="Show Next L-M", command=inc_counter_lm)
lpbutton = tk.Button(root, text="Show Next L-P", command=inc_counter_lp)
counter_text = tk.Label(root, textvariable=v)

file = tk.StringVar(root)
# initial value
file.set('Choose File')
filenames = [f for f in listdir('./benchmarks/') if isfile(join('./benchmarks/', f))]
drop = tk.OptionMenu(root, file, *filenames)
drop.pack(side='left', padx=10, pady=10)
go = tk.Button(root, text="Choose File", command=read_infile)
go.pack(side='left', padx=20, pady=10)


var = tk.StringVar(root)
# initial value
var.set('Choose Routing Algorithm')
choices = ['Lee Moore', 'Line Probe']
option = tk.OptionMenu(root, var, *choices)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="Start Route", command=route)
button.pack(side='left', padx=20, pady=10)

root.mainloop()
from os import listdir
from os.path import isfile, join, basename

dirname = './output/'
outdir = './testnets/'

filenames = [f for f in listdir(dirname) if isfile(join(dirname, f)) and ".blif" in f]

for f in filenames:
	print f
	nets = {}
	inet = 0
	cells = []
	with open(join(dirname,f)) as of:
		temp = []
		# INPUTS
		line = of.readline()
		while (line):
			if ".inputs " in line:
				break
			line = of.readline()
		temp = [i for i in line.split()]
		while "\\" in temp:
			del temp[temp.index("\\")]
			line = of.readline()
			temp = temp + [i for i in line.split()]
		del temp[temp.index(".inputs")]
		for net in temp:
			nets[net] = inet 
			inet = inet + 1
		temp = []
		# OUTPUTS
		line = of.readline()
		while (line):
			if ".outputs " in line:
				break
			line = of.readline()
		temp = [i for i in line.split()]
		while "\\" in temp:
			del temp[temp.index("\\")]
			line = of.readline()
			temp = temp + [i for i in line.split()]
		del temp[temp.index(".outputs")]
		for net in temp:
			if net not in nets:
				nets[net] = inet
				inet = inet + 1
			else:
				print net + "output already in nets?"
		temp = []
		# INTERNAL SIGNALS
		line = of.readline()
		while (line):
			connects = []
			if ".barbuf" in line:
				connects = [i for i in line.split()]
				del connects[connects.index(".barbuf")]
			else:
				while "=" in line:
					start = line.find('=') + 1
					end = line.find(' ', start)
					connects = connects + [line[start:end]]
					line = line[end:]
			if "end" not in line:
				temp = temp + connects
				cells = cells + [connects]
			line = of.readline()
		for net in temp:
			if net not in nets:
				nets[net] = inet 
				inet = inet + 1
	with open(join(outdir,basename(f.split('.')[0])+'.txt'),"w+") as of:
		of.write(str(len(cells))+' '+str(len(nets))+' 12 12\n')
		#print str(len(cells))+' '+str(len(nets))
		for cell in cells:
			temp = ''
			temp = temp + str(len(cell))+' '
			for net in cell:
				temp = temp + str(nets[net])+' '
			of.write(temp+'\n')
			#print temp


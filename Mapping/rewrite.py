"""
rewrite.py
rewrites mapped benchmark circuits into input format expected by placement algorithm
TODO doesn't handle input/output nets well yet - no cells allocated as input/output pins

"""

from os import listdir
from os.path import isfile, join, basename

dirname = './Mapping/output/'
outdir = './Mapping/testnets/'

filenames = [f for f in listdir(dirname) if isfile(join(dirname, f)) and ".blif" in f]

for f in filenames:
	print f
	nets = {}
	inet = 0
	cells = []
	inputs = []
	outputs = []
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
		inputs = [i for i in temp]
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
		outputs = [i for i in temp]
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
		output = []
		#of.write(str(len(cells))+' '+str(len(nets))+' 12 12\n')
		#print str(len(cells))+' '+str(len(nets))

		# one line per net
		# each line contains number of blocks connected by net
		# successive numbers are the block id numbers connected by that net
		# net is net name string, nets[net] is net id number
		numnets = 0
		for net in nets:
			# find source of net (check that there is only 1)
			source = []
			for i,cell in enumerate(cells):
				if cell[-1] == net:
					source.append(i)
			if len(source) > 1:
				print "more than 1 source"
				print net
			# find sinks of net
			sinks = []
			for i,cell in enumerate(cells):
				if net in cell[:-1]:
					sinks.append(i)
			if len(source) == 1 and len(sinks) >= 1:
				numnets = numnets + 1
				line = str(1+len(sinks))
				line += ' '
				line += str(source[0]) 
				line += ' '
				for sink in sinks:
					line += str(sink) 
					line += ' '
				line += '\n'
				output.append(line)

		of.write(str(len(cells))+ ' ' +str(numnets)+ ' 12 12\n')
		of.write(str(len(inputs))+'\n')
		for each in inputs:
			temp_str = ''
			sinks = []
			for i,cell in enumerate(cells):
				if each in cell[:-1]:
					sinks.append(i)
			if len(sinks) >= 1:
				for sink in sinks:
					temp_str = temp_str + str(sink) + ' '
				of.write(temp_str + '\n')
		of.write(str(len(outputs))+'\n')
		for each in outputs:
			source = []
			for i,cell in enumerate(cells):
				if cell[-1] == each:
					source.append(i)
			if len(source) > 1:
				print "more than 1 source"
			else:
				of.write(str(source[0]) + '\n')
		for each in output:
			of.write(each)


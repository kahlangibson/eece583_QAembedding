"""
Connection graph
		1 ----- 2
		| \   / |
		|   X   |
		| /   \ |
		4 ----- 3

		1 1 - 2 
		2 1 - 3
		3 1 - 4
		4 2 - 3 
		5 2 - 4
		6 3 - 4

"""

class logic_qbit(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.qbit = {}
		# initialize logic qbit weight
		for i in range(1,5):
			self.qbit[i] = 0
		# initially no wires
		# wires
		self.wire = {}
		for i in range(1,7):
			self.wire[i] = 0
		self.north_bus = [0,0,0,0]
		self.south_bus = [0,0,0,0]
		self.east_bus = [0,0,0,0]
		self.west_bus = [0,0,0,0]


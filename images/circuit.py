from logic_qbit import logic_qbit

class circuit(object):
	def __init__(self):
		self.grid = {}
		for _x in range(12):
			for _y in range(12):
				self.grid[_x,_y] = logic_qbit(_x,_y)



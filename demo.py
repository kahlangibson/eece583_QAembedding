from circuit import circuit
from PIL import Image, ImageDraw
from os import listdir
from os.path import isfile, join

# perform circuit initialization
# TODO
circuit = circuit()

# make picture
height = 1200
width = 1200

deltay = height/12
deltax = width/12

circlex = deltax/5
circley = deltay/3

radius = circlex/3

image = Image.new('RGB', size=(height,width), color='white')
draw = ImageDraw.Draw(image)

fill = 128

for _x in range(12):
	for _y in range(12):
		for _cy in range(2):
			for _cx in range(4):
				x = _x * deltax + _cx * circlex + deltax/4
				y = _y * deltay + _cy * circley + deltay/4
				draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline='gray', fill='white')
		for _pair in range(4):
			x = _x * deltax + _pair * circlex + deltax/4
			y1 = _y * deltay + deltay/4
			y2 = _y * deltay + 1 * circley + deltay/4
			draw.line((x, y1+radius, x, y2-radius ), fill='#C0C0C0')
		for _set in range(3):
			for _pair in range(_set+1,4):
				x1 = _x * deltax + _set * circlex + deltax/4
				ya = _y * deltay + deltay/4
				yb = _y * deltay + 1 * circley + deltay/4
				x2 = _x * deltax + _pair * circlex + deltax/4
				draw.line((x1, ya+radius, x2, yb-radius ), fill='#C0C0C0')
				draw.line((x1, yb-radius, x2, ya+radius ), fill='#C0C0C0')
for _channel in range(4):
	# vertical
	for _y in range(11):
		for _x in range(12):
			x = _x * deltax + (_channel+1) * circlex + deltax/4
			ya = _y * deltay + deltay/4
			yb = (_y+1) * deltay + deltay/4
			draw.arc((x-radius-deltax/3,ya,x-radius,yb), 90, 270, fill='#C0C0C0')

	# horizontal
	for _y in range(12):
		for _x in range(11):
			y = _y * deltay + deltay/2 - 2*radius
			xa = _x * deltax + (_channel) * circlex + deltax/4
			xb = (_x+1) * deltax + (_channel) * circlex + deltax/4
			draw.arc((xa,y-deltay/3,xb,y), 180, 0, fill='#C0C0C0')

# with open("demoplaced.txt") as f:
# 	f.readline()
# 	cells = int(f.readline())
# 	for _ in range(cells):
# 		data = [int(s) for s in f.readline().split()]
# 		# draw box at data[0], data[1]
# 		print str(data[0]) + ' ' + str(data[1])
# 		x1 = data[0] * deltax + deltax/8
# 		x2 = (data[0]+1) * deltax
# 		y1 = data[1] * deltay + deltay/8
# 		y2 = (data[1]+1) * deltay - deltay/4
# 		print str(x1) + ' ' + str(y1)
# 		print str(x2) + ' ' + str(y2)
# 		draw.rectangle((x1, y1, x2, y2), outline='blue', fill=None)
# 		draw.rectangle((x1-1, y1-1, x2+1, y2+1), outline='blue', fill=None)

with open("demo.txt") as f:
	cells = {}

	ncells = int(f.readline())
	for _ in range(ncells):
		data = [int(s) for s in f.readline().split()]
		cells[data[0],data[1]] = []

	ins = int(f.readline())
	for _ in range(ins):
		data = [int(s) for s in f.readline().split()]
		channel = data[0]
		numcells = data[1]
		for i in range(2,2+2*numcells,2):
			x1 = data[i]
			y1 = data[i+1]
			if (x1,y1) in cells:
				cells[x1,y1].append(channel)
			x = x1 * deltax + channel * circlex + deltax/4
			ya = y1 * deltay + deltay/4
			draw.ellipse((x-radius, ya-radius, x+radius, ya+radius), outline='gray', fill='magenta')
			yb = y1 * deltay + circley + deltay/4
			draw.ellipse((x-radius, yb-radius, x+radius, yb+radius), outline='gray', fill='magenta')
			draw.line((x, ya+radius, x, yb-radius ), fill='#008B8B')
			draw.line((x-1, ya+radius, x-1, yb-radius ), fill='#008B8B')

	outs = int(f.readline())
	for _ in range(outs):
		data = [int(s) for s in f.readline().split()]
		channel = data[0]
		numcells = data[1]
		for i in range(2,2+2*numcells,2):
			x1 = data[i]
			y1 = data[i+1]
			if (x1,y1) in cells:
				cells[x1,y1].append(channel)
			x = x1 * deltax + channel * circlex + deltax/4
			ya = y1 * deltay + deltay/4
			draw.ellipse((x-radius, ya-radius, x+radius, ya+radius), outline='gray', fill='magenta')
			yb = y1 * deltay + circley + deltay/4
			draw.ellipse((x-radius, yb-radius, x+radius, yb+radius), outline='gray', fill='magenta')
			draw.line((x, ya+radius, x, yb-radius ), fill='#008B8B')
			draw.line((x-1, ya+radius, x-1, yb-radius ), fill='#008B8B')

	nets = int(f.readline())
	for _ in range(nets):
		data = [int(s) for s in f.readline().split()]
		channel = data[0]
		numcells = data[1]
		for i in range(2,2+2*(numcells-1),2):
			x1 = data[i]
			y1 = data[i+1]
			if (x1,y1) in cells:
				cells[x1,y1].append(channel)
			x2 = data[i+2]
			y2 = data[i+3]
			x = x1 * deltax + channel * circlex + deltax/4
			ya = y1 * deltay + deltay/4
			draw.ellipse((x-radius, ya-radius, x+radius, ya+radius), outline='gray', fill='cyan')
			yb = y1 * deltay + circley + deltay/4
			draw.ellipse((x-radius, yb-radius, x+radius, yb+radius), outline='gray', fill='cyan')
			draw.line((x, ya+radius, x, yb-radius ), fill='#008B8B')
			draw.line((x-1, ya+radius, x-1, yb-radius ), fill='#008B8B')
			if (y1 == y2):
				y = y1 * deltay + deltay/2 - 2*radius
				xa = x1 * deltax + channel * circlex + deltax/4
				xb = x2 * deltax + channel * circlex + deltax/4
				if (xa > xb):
					draw.arc((xb,y-deltay/3,xa,y), 180, 0, fill='#008B8B')
					draw.arc((xb,y-1-deltay/3,xa,y-1), 180, 0, fill='#008B8B')
				else:
					draw.arc((xa,y-deltay/3,xb,y), 180, 0, fill='#008B8B')
					draw.arc((xa,y-1-deltay/3,xb,y-1), 180, 0, fill='#008B8B')
			if (x1 == x2):
				x = x1 * deltax + (channel+1) * circlex + deltax/4
				ya = y1 * deltay + deltay/4
				yb = y2 * deltay + deltay/4
				if (ya > yb):
					draw.arc((x-radius-deltax/3,yb,x-radius,ya), 90, 270, fill='#008B8B')
					draw.arc((x-1-radius-deltax/3,yb,x-1-radius,ya), 90, 270, fill='#008B8B')
				else:
					draw.arc((x-radius-deltax/3,ya,x-radius,yb), 90, 270, fill='#008B8B')
					draw.arc((x-1-radius-deltax/3,ya,x-1-radius,yb), 90, 270, fill='#008B8B')
		if (data[-2],data[-1]) in cells:
			cells[data[-2],data[-1]].append(channel)
		x = data[-2] * deltax + channel * circlex + deltax/4
		ya = data[-1] * deltay + deltay/4
		draw.ellipse((x-radius, ya-radius, x+radius, ya+radius), outline='gray', fill='cyan')
		yb = data[-1] * deltay + circley + deltay/4
		draw.ellipse((x-radius, yb-radius, x+radius, yb+radius), outline='gray', fill='cyan')
		draw.line((x, ya+radius, x, yb-radius ), fill='#008B8B')
		draw.line((x-1, ya+radius, x-1, yb-radius ), fill='#008B8B')

	for (x,y) in cells:
		for j in range(len(cells[x,y])-1):
			for i in range(j+1,len(cells[x,y])):
				x1 = x * deltax + cells[x,y][j] * circlex + deltax/4
				ya = y * deltay + deltay/4
				yb = y * deltay + 1 * circley + deltay/4
				x2 = x * deltax + cells[x,y][i] * circlex + deltax/4
				draw.line((x1, ya+radius, x2, yb-radius ), fill='#008B8B')
				draw.line((x1, yb-radius, x2, ya+radius ), fill='#008B8B')
				draw.line((x1-1, ya+radius, x2-1, yb-radius ), fill='#008B8B')
				draw.line((x1-1, yb-radius, x2-1, ya+radius ), fill='#008B8B')


image.show()


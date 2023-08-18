from neuro import NeuralNetwork
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import asyncio

mind = NeuralNetwork([25, 4])
canvas_size = 1280
realsize = 32

pix = canvas_size / realsize

canvas = [[0.1 for x in range(realsize)] for y in range(realsize)]
cellx, celly = 15, 5


def cellvision(vis):
	global cellx
	global celly
	global canvas
	inp = []

	if vis != -1:
		for j in range(vis):
			for i in range(vis):
				inp.append(canvas[int(cellx - vis // 2 + i) % realsize][int(celly - vis // 2 + j) % realsize])
		return inp

	inp.append(canvas[int(cellx + 0) % realsize][int(celly - 1) % realsize])
	inp.append(canvas[int(cellx + -1) % realsize][int(celly + 0) % realsize])
	inp.append(canvas[int(cellx + 1) % realsize][int(celly + 0) % realsize])
	inp.append(canvas[int(cellx + 0) % realsize][int(celly + 1) % realsize])

	return inp


def move(out):
	global cellx
	global celly
	if out == 0:
		celly -= 1
	if out == 1:
		cellx -= 1
	if out == 2:
		cellx += 1
	if out == 3:
		celly += 1
	if cellx == realsize:
		cellx = 0
	if cellx == -1:
		cellx = realsize - 1
	if celly == realsize:
		celly = 0
	if celly == -1:
		celly = realsize - 1
	cell(cellx, celly)
	return


def goodpoint(x, y):
	color = "#476042"
	x, y = x * pix, y * pix
	x1, y1 = (x - pix / 2), (y - pix / 2)
	x2, y2 = (x + pix / 2), (y + pix / 2)
	w.create_oval(x1, y1, x2, y2, outline=color, fill=color)


def badpoint(x, y):
	color = "#ff0000"
	x, y = x * pix, y * pix
	x1, y1 = (x - pix / 2), (y - pix / 2)
	x2, y2 = (x + pix / 2), (y + pix / 2)
	w.create_oval(x1, y1, x2, y2, outline=color, fill=color)


def cell(x, y):
	color = "#ffffff"
	x, y = x * pix, y * pix
	x1, y1 = (x - pix / 2), (y - pix / 2)
	x2, y2 = (x + pix / 2), (y + pix / 2)
	w.create_oval(x1, y1, x2, y2, outline=color, fill=color)


def canvas_print():
	global canvas
	w.delete("all")
	ans = ''
	for y in range(realsize):
		for x in range(realsize):
			ans += str(canvas[x][y]) + " "
			if canvas[x][y] == 1:
				goodpoint(x, y)
			if canvas[x][y] == -1:
				badpoint(x, y)
			if canvas[x][y] == 0:
				cell(x, y)
		ans += "\n"


def usergoodpoint(event):
	x, y = int(event.x / pix), int(event.y / pix)
	canvas[x][y] = 1


def userbadpoint(event):
	x, y = int(event.x / pix), int(event.y / pix)
	canvas[x][y] = -1


master = Tk()
master.title("Среда обучения")
w = Canvas(master, bg="black",
		   width=canvas_size,
		   height=canvas_size)
w.pack(expand=YES, fill=BOTH)
w.bind("<B1-Motion>", usergoodpoint)
w.bind("<B3-Motion>", userbadpoint)

iterat = -1
allg = 0
graphic = []
while True:
	iterat += 1
	if iterat % 200 == 0:
		plt.plot(graphic)
		plt.pause(0.0000001)
	good = 0

	if iterat % 10000 == 0:
		plt.close()
		mind.show()

	canvas[random.randint(0, realsize - 1)][random.randint(0, realsize - 1)] = 1
	canvas[random.randint(0, realsize - 1)][random.randint(0, realsize - 1)] = -1

	canvas_print()

	visn = cellvision(5)
	visnn = cellvision(-1)

	out = mind.out(visn)
	move_ = out[-1].index(max(out[-1]))
	mind.correct(visn, visnn, 0.1)

	answer = [0]*4
	answer[move_] = 1
	move(move_)

	if canvas[cellx][celly] == 1:
		good += 50
		canvas[cellx][celly] = 0.1

	elif canvas[cellx][celly] == -1:
		good -= 50
		canvas[cellx][celly] = 0.1

	# print(input())
	allg += good
	graphic.append(allg)

	master.title("Среда обучения: " + " i:" + str(iterat) + " good:" + str(good))
	master.update()

plt.show()
master.mainloop()

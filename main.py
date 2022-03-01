import asyncio
from tkinter import *
import matplotlib.pyplot as plt
import aneuro
import random
import os

mind = aneuro.create_network([25, 25, 25, 25, 50, 100, 250, 300, 250, 100,50, 25, 10, 5])

canvas_size = 1280
realsize = 32

pix = canvas_size / realsize

canvas = [[0.1 for x in range(realsize)] for y in range(realsize)]
cellx, celly = realsize // 2, realsize // 2
zerox, zeroz = pix / 2, pix / 2


def cellvision(vis):
    global cellx
    global celly
    global canvas
    inp = []

    for j in range(vis):
        for i in range(vis):
            inp.append(canvas[int(cellx - vis // 2 + j) % realsize][int(celly - vis // 2 + i) % realsize])
    return(inp)

async def pos(w, x, y):
    color = "#65b2c6"
    x, y = x * pix, y * pix
    x1, y1 = zerox + (x - pix / 2), zeroz + (y - pix / 2)
    x2, y2 = zerox + (x + pix / 2), zeroz + (y + pix / 2)
    w.create_oval(x1, y1, x2, y2, outline=color, fill=color)


async def neg(w, x, y):
    color = "#d73d6c"
    x, y = x * pix, y * pix
    x1, y1 = zerox + (x - pix / 2), zeroz + (y - pix / 2)
    x2, y2 = zerox + (x + pix / 2), zeroz + (y + pix / 2)
    w.create_oval(x1, y1, x2, y2, outline=color, fill=color)


def cell(w, x, y):
    color = "#c0cccc"
    x, y = x * pix, y * pix
    x1, y1 = zerox + (x - pix / 2), zeroz + (y - pix / 2)
    x2, y2 = zerox + (x + pix / 2), zeroz + (y + pix / 2)
    w.create_oval(x1, y1, x2, y2, outline=color, fill=color)


def move(out):
    global cellx
    global celly
    if out == 0:
        celly -= 1
    if out == 1:
        celly += 1
    if out == 2:
        cellx += 1
    if out == 3:
        cellx -= 1
    cellx = cellx%realsize
    celly = celly%realsize
    cell(w, cellx, celly)


async def canvas_print():
    global canvas
    w.delete("all")
    future_queue=[]
    for y in range(realsize):
        for x in range(realsize):
            if canvas[x][y] == 1:
                future_queue.append(pos(w, x, y))
            if canvas[x][y] == -1:
                future_queue.append(neg(w, x, y))
    for el in future_queue:
        await el
    cell(w, cellx, celly)


master = Tk()
master.title("Среда обучения")
w = Canvas(master, bg="#27282d",
           width=canvas_size,
           height=canvas_size)
w.pack(expand=YES, fill=BOTH)



for i in range(realsize):
    for j in range(realsize):
        # random.choice([pos, neg])(i, j)
        master.update()

for it in range(0):
    out = aneuro.out(mind.out(cellvision(5)))
    #print(out)
    for i in range(int(realsize ** (1 / 3))):
        canvas[random.randint(0, realsize - 1)][random.randint(0, realsize - 1)] = random.choice([1, -1])

    if canvas[cellx][celly] == 1:
        mind.reinfor(cellvision(5), 0.003)
        canvas[cellx][celly] = 0.1

    if canvas[cellx][celly] == -1:
        mind.reinfor(cellvision(5), -0.1)
        canvas[cellx][celly] = 0.1

    if canvas[cellx][celly] == 0.1:
        mind.reinfor(cellvision(5), -0.001)
        canvas[cellx][celly] = 0.1

    master.title("Среда обучения: " + " i:" + str(it))
    master.update()


print(canvas)
async def env():
    global realsize
    global canvas_size
    global canvas
    global pix
    global zerox
    global zeroz
    it = 0
    stp = 0
    stn = 0
    while True:
        if False:
            realsize *= 2

            pix = canvas_size / realsize

            zerox, zeroz = pix / 2, pix / 2

            canvas = [[0.1 for x in range(realsize)] for y in range(realsize)]
        if it % 100==0:
            print(stp, " - ", stn, " ", (stp/stn if stn != 0 else 0),"%")
            stp, stn = 0,0
        cor = canvas_print()

        out = aneuro.out(mind.out(cellvision(5)))
        #print(out)
        move(out)
        for i in range(2):
            canvas[random.randint(0, realsize - 1)][random.randint(0, realsize - 1)] = random.choice([1, -1])

        if canvas[cellx][celly] == 1:
            mind.reinfor(cellvision(5), 0.003)
            canvas[cellx][celly] = 0.1
            stp+=1

        if canvas[cellx][celly] == -1:
            mind.reinfor(cellvision(5), -0.1)
            canvas[cellx][celly] = 0.1
            stn+=1

        if canvas[cellx][celly] == 0.1:
            mind.reinfor(cellvision(5), -0.001)
            canvas[cellx][celly] = 0.1

        await cor
        master.title("Среда обучения: " + " i:" + str(it))
        master.update()
        it+=1

asyncio.run(env())
plt.show()
master.mainloop()

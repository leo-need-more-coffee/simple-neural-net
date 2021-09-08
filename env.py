from tkinter import *
import matplotlib.pyplot as plt
import neurocell
import random

mind=neurocell.create_network([5*5,16],4)

canvas_size=640
realsize=16

pix=canvas_size/realsize

canvas=[[0.1 for x in range(realsize)] for y in range(realsize)]
cellx,celly=15,15
aix,aiy,=15,15

def cellvision(vis):
	global cellx
	global celly
	global canvas
	inp=[]
	if vis !=-1:
		for i in range(vis):
			for j in range(vis):
				if int(cellx-vis//2+1+j) >= realsize-1 and int(celly-vis//2+1+i) >= realsize-1 and int(cellx-vis//2+1+j) <= 0  and int(celly-vis//2+1+i) <= 0:
					inp.append(canvas[int(cellx-vis//2+1+j)][int(celly-vis//2+1+i)])
				else:
					inp.append(0)
			#print()
	else:
		if cellx >= realsize-1 and celly-1 >= realsize-1 and cellx <= 0 and celly-1 <= 0:
			inp.append(canvas[cellx][celly-1])
		else:
			inp.append(0)
		if cellx >= realsize-1 and celly+1 >= realsize-1 and cellx <= 0 and celly+1 <= 0:
			inp.append(canvas[cellx][celly+1])
		else:
			inp.append(0.1)
		if cellx+1 >= realsize-1 and celly >= realsize-1 and cellx+1 <= 0 and celly <= 0:
			inp.append(canvas[cellx+1][celly])
		else:
			inp.append(0.1)
		if cellx-1 >= realsize-1 and celly >= realsize-1 and cellx-1 <= 0 and celly <= 0:
			inp.append(canvas[cellx-1][celly])
		else:
			inp.append(0.1)

	return(inp)

def move(out):
	global cellx
	global celly
	if out==0:
		celly-=1
	if out==1:
		celly+=1
	if out==2:
		cellx+=1
	if out==3:
		cellx-=1
	if cellx==realsize:
		cellx=1
	if cellx==0:
		cellx=realsize-1
	if celly==realsize:
		celly=1
	if celly==0:
		celly=realsize-1
	cell(cellx,celly)
	return

def goodpoint(x,y):
	color = "#476042"
	x,y=x*pix,y*pix
	x1, y1 = ( x - pix/2 ), ( y - pix/2 )
	x2, y2 = ( x + pix/2 ), ( y + pix/2 )
	w.create_oval( x1, y1, x2, y2, outline=color,fill = color )

def badpoint(x,y):
	color = "#ff0000"
	x,y=x*pix,y*pix
	x1, y1 = ( x - pix/2 ), ( y - pix/2 )
	x2, y2 = ( x + pix/2 ), ( y + pix/2 )
	w.create_oval( x1, y1, x2, y2, outline=color,fill = color )

def cell(x,y):
	color = "#ffffff"
	x,y=x*pix,y*pix
	x1, y1 = ( x - pix/2 ), ( y - pix/2 )
	x2, y2 = ( x + pix/2 ), ( y + pix/2 )
	w.create_oval( x1, y1, x2, y2, outline=color,fill = color )

def canvas_print():
	global canvas
	w.delete("all")
	ans=''
	for y in range(realsize):
		for x in range(realsize):
			ans+=str(canvas[x][y])+" "
			if canvas[x][y] == 1:
				goodpoint(x,y)
			if canvas[x][y] == -1:
				badpoint(x,y)
			if canvas[x][y] == 0:
				cell(x,y)
		ans+="\n"

def usergoodpoint(event):
	x,y=int(event.x/pix),int(event.y/pix)
	canvas[x][y]=1

def userbadpoint(event):
	x,y=int(event.x/pix),int(event.y/pix)
	canvas[x][y]=-1

master = Tk()
master.title( "Среда обучения" )
w = Canvas(master, bg="black",
           width=canvas_size,
           height=canvas_size)
w.pack(expand = YES, fill = BOTH)
w.bind( "<B1-Motion>", usergoodpoint )
w.bind( "<B3-Motion>", userbadpoint )

iterat=-1
allg=0
graphic=[]
rev=True
neurocell.defch=input("Введите число(дефолт - 0.01):")
if neurocell.defch=="":
	neurocell.defch=0.01
else:
	neurocell.defch=float(neurocell.defch)
end=input("кол-во ходов:")
if end=="":
	end=-1
else:
	end=int(end)+1
revv=input("реверс на ходу:")
if revv=="":
	revv=-1
else:
	revv=int(revv)+1

while True:
	iterat += 1
	if iterat == end:
		break
	if iterat==revv:
		rev=False
	if iterat%200==0:
		plt.plot(graphic)
		plt.pause(0.0000001)
	good=0
	if rev:
		canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=1
		canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=1
		canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=-1
	else:
		canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=1
		canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=-1
		canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=-1
	canvas_print()
	
	visn=cellvision(5)
	visnn=cellvision(-1)
	if rev:
		if iterat!=0:
			for i in range(len(visnn)):
				if visnn[i]==1:
					mind.good(i,50)
				if visnn[i]==-1:
					mind.bad(i,50)
				else:
					mind.bad(i,10)
	else:
		if iterat!=0:
			for i in range(len(visnn)):
				if visnn[i]==1:
					mind.bad(i, 50)
				if visnn[i]==-1:
					mind.good(i,50)
				else:
					mind.bad(i,10)
	out=mind.out(visn)
	move(out)

	if rev:
		if canvas[cellx][celly]==1:
			good+=50
			canvas[cellx][celly]=0.1
		elif canvas[cellx][celly]==-1:
			good-=50
			canvas[cellx][celly]=0.1
		else:
			good-=10
	else:
		if canvas[cellx][celly]==1:
			good-=50
			canvas[cellx][celly]=0.1
		elif canvas[cellx][celly]==-1:
			good+=50
			canvas[cellx][celly]=0.1
		else:
			good-=10
	#print(input())
	allg+=good
	graphic.append(allg)
	if rev:
		plt.suptitle("График обучения при условии: 1 единица подкрепления = "+str(neurocell.defch)+" изменения весов")
	else:
		plt.suptitle("График обучения при условии: 1 единица подкрепления = " + str(neurocell.defch) + " изменения весов\n Изменение правил произошло на ходу "+str(revv))
	master.title( "Среда обучения: "+" i:"+ str(iterat)+" good:"+str(good))
	master.update()
plt.show()
master.mainloop()
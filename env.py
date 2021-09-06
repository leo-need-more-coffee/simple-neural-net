from tkinter import *
import random
import neurocell
import matplotlib.pyplot as plt
import os
import itertools
import networkx as nx

mind=neurocell.create_network([5*5,16],4)

graph = nx.Graph()
subset_sizes = [5*5, 16, 4]
subset_color = [
    "gold",
    "limegreen",
    "limegreen",
    "darkorange",
]


def multilayered_graph(*subset_sizes):
    extents = nx.utils.pairwise(itertools.accumulate((0,) + subset_sizes))
    layers = [range(start, end) for start, end in extents]
    G = nx.Graph()
    for (i, layer) in enumerate(layers):
        G.add_nodes_from(layer, layer=i)
    for layer1, layer2 in nx.utils.pairwise(layers):
        G.add_edges_from(itertools.product(layer1, layer2))
    return G


G = multilayered_graph(*subset_sizes)
color = [subset_color[data["layer"]] for v, data in G.nodes(data=True)]
pos = nx.multipartite_layout(G, subset_key="layer")
plt.figure(figsize=(8, 8))
nx.draw(G, pos, node_color=color, with_labels=False)
#plt.axis("equal")
plt.show()



canvas_size=640
realsize=16

pix=canvas_size/realsize

canvas=[[0.1 for x in range(realsize)] for y in range(realsize)] 
cellx,celly=15,15
aix,aiy,=15,15

canvas_width = canvas_size
canvas_height = canvas_size


def cellvision(vis):
	global cellx
	global celly
	global canvas
	inp=[]
	if vis !=-1:
		for i in range(vis):
			for j in range(vis):
				try:
					inp.append(canvas[int(cellx-vis/2+1+j)][int(celly-vis/2+1+i)])
					#auto(int(cellx-vis/2+1+j),int(celly-vis/2+1+i))
					#print(canvas[int(cellx-vis/2+j)][int(celly-vis/2+i)]," ",end="")
				except:
					inp.append(0.1)
			#print()
	else:
		try:
			inp.append(canvas[cellx][celly-1])
		except:
			inp.append(0.1)
		try:
			inp.append(canvas[cellx][celly+1])
		except:
			inp.append(0.1)
		try:
			inp.append(canvas[cellx+1][celly])
		except:
			inp.append(0.1)
		try:
			inp.append(canvas[cellx-1][celly])
		except:
			inp.append(0.1)

	return(inp)
def automove(out):
	global aix
	global aiy
	if out==0:
		aiy-=1
	if out==1:
		aiy+=1
	if out==2:
		aix+=1
	if out==3:
		aix-=1
	if aix==realsize:
		aix=1
	if aix==0:
		aix=realsize-1
	if aiy==realsize:
		aiy=1
	if aiy==0:
		aiy=realsize-1		
	auto(aix,aiy)
	return

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

def auto(x,y):
	color = "#ffff00"
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
master.title( "Чашка Петри" )
w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
w.pack(expand = YES, fill = BOTH)
#w.bind( "<G>", mind.good(-1,100) )
#w.bind( "<B>", mind.bad(-1,100) )
w.bind( "<B1-Motion>", usergoodpoint )
w.bind( "<B3-Motion>", userbadpoint )

neurogood=0
autogood=0
co=0
iterat=-1
allg=0
log=[]
log1=[]
log2=[]
while True:
	if iterat%50==0:
		print(log)
		plt.plot(log2)
		plt.pause(0.0001)
	iterat+=1
	print()
	good=0
	canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=1
	canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=1
	canvas[random.randint(0,realsize-1)][random.randint(0,realsize-1)]=-1

	canvas_print()
	
	visn=cellvision(5)
	visnn=cellvision(-1)
	print(visnn)
	if iterat!=0:
		for i in range(len(visnn)):
			if visnn[i]==1:
				print(i,visnn[i])
				mind.good(i,50)
			if visnn[i]==-1:
				mind.bad(i,50)
			else:
				mind.bad(i,10)	

	out=mind.out(visn)
	move(out)

	
	if canvas[cellx][celly]==1:
		neurogood+=1
		#mind.good(-1,100)
		good+=50
		canvas[cellx][celly]=0.1
	elif canvas[cellx][celly]==-1:
		neurogood-=1
		#mind.bad(-1,100)
		good-=50
		canvas[cellx][celly]=0.1
	else:
		#mind.bad(-1,20)
		good-=10
	#print(input())
	allg+=good
	log2.append(allg)

	master.title( "Чашка Петри: "+" i:"+ str(iterat)+" good:"+str(good)+" neuro:"+str(neurogood)+" auto:"+str(autogood)+" co:"+str(co))
	print(good,"очков положительного подкрепления за этот ход")
	master.update()
plt.show()
master.mainloop()
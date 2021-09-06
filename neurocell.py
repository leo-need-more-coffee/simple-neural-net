import random
import math

done=-1
layers=[]

def okr(num):
    #num = int(num + (0.5 if num > 0 else -0.5))
    return num

def act(num):
    try:
        return(math.tanh(num))
    except OverflowError:
        return(0)


class Neuron(object):
    def __init__(self, childs, weight,isultra):
        self.childs = childs
        self.weight = weight
        self.isultra=isultra
        self.out=None

    def getout(self,input):
        if self.isultra:
            out=0
            for i in range(len(input)):
                self.childs[i].out=input[i]
                out+=act(act(self.childs[i].out)*self.childs[i].weight)

            self.out=act(out)
            #print(self.out)
            return(self.out)
        else:
            out=0
            for i in range(len(self.childs)):
                out+=act(self.childs[i].getout(input)*self.childs[i].weight)
            self.out=act(out)
            return(self.out)

    def chweight(self,mlt):
        if self.isultra:
            for i in range(len(self.childs)):
                if self.childs[i].out>=0.5:
                    self.childs[i].weight+=mlt
                if self.childs[i].out<=-0.5:
                    self.childs[i].weight-=mlt               
            if self.out>=0.5:
                self.weight+=mlt
            if self.out<=-0.5:
                self.weight-=mlt 
        else:
            for i in range(len(self.childs)):
                self.childs[i].chweight(mlt)
            if self.out>=0.5:
                self.weight+=mlt
            if self.out<=-0.5:
                self.weight-=mlt 
        return

class Mind(object):
    def __init__(self, childs):
        self.outs = childs

    def out(self,input):
        maxx,indx=-1,None
        maxxlist=list()
        for i in range(len(self.outs)):
            now=self.outs[i].getout(input)
            '''
            if i==0:
                print("▲",okr(now*10)/10)
            if i==1:
                print("▼",okr(now*10)/10)
            if i==2:
                print("ᐅ",okr(now*10)/10)
            if i==3:
                print("ᐊ",okr(now*10)/10)
            '''
            if now==maxx:
                   maxxlist.append(i)
            if now> maxx:
                maxx=now
                maxxlist=[i]
                
        return(random.choice(maxxlist))
    def bad(self,out,cof):
        if out ==-1:
            for i in range(len(self.outs)):
                self.outs[i].chweight(-0.0001*cof/len(self.outs))
        else:
            self.outs[out].chweight(-0.0001*cof)
        return True
    def good(self,out,cof):
        if out ==-1:
            for i in range(len(self.outs)):
                self.outs[i].chweight(0.0001*cof/len(self.outs))
        else:
            self.outs[out].chweight(0.0001*cof)
        return True

def create_neuron(layers):
    if len(layers)==1:
        global done
        
        if done%1000==0:
            print(done,"/",16*16*16*4)
        neuron=Neuron([],random.uniform(-0.5,0.5),True)
        for j in range(layers[-1]):
            done+=1
            neuron.childs.append(Neuron(None,random.uniform(-0.5,0.5),False))
        return neuron
    else:
        done+=1
        neuron=Neuron([],random.uniform(-0.5, 0.5),False)
        for j in range(layers[-1]):
            neuron.childs.append(create_neuron(layers[:-1]))
        return neuron

def create_network(layers,p):
    mind=Mind([])
    for i in range(p):
        mind.outs.append(create_neuron(layers))
    return(mind)

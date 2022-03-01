import numpy as np
import asyncio
import math, random

eps = 0.3

def act(a):
    return math.tanh(a)

class Network():
    def __init__(self, network_, shape_):
        self.sinaps = network_
        self.shape = shape_

    def out(self, input_):
        input = np.array(input_)
        #print(input)
        for i in range(len(self.shape)-1):
            input = [act(np.sum((self.sinaps[i][j]*input))) for j in range(self.shape[i+1])]
            #print(input)
        return input

    def reinfor(self, input_, multiplier):
        input = np.array(input_)
        #print(input)
        for i in range(len(self.shape)-1):
            input = [act(np.sum((self.sinaps[i][j]*input))) for j in range(self.shape[i+1])]
            for j in range(self.shape[i+1]):
                if abs(input[j])>eps:
                    self.sinaps[i][j] += multiplier * (input[j]/abs(input[j]))
                else:
                    self.sinaps[i][j] += random.choice([multiplier * random.choice([1, -1]), 0, 0])

        return input


def out(input):
    index, max_value = max(enumerate(input), key=lambda i_v: i_v[1])
    return index

def create_network(network_shape):
    network_ = []
    for i in range(len(network_shape)-1):
        network_.append(np.random.random((network_shape[i+1], network_shape[i]))*2-1)
    network = Network(network_, network_shape)
    return network


net = create_network([5,4,3,2])
print(net.sinaps)

net.reinfor([1,1,1,1,1],1)

print(net.sinaps)
print(out(net.out([1,0,0,1,0])))
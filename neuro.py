import math
import random
import time
import datetime
import json
from copy import copy

activation = math.tanh
deactivation = math.tanh


class NeuralNetwork:
    def __init__(self, neurons_size: list, weights: list = None):
        self.neuron_size = neurons_size
        for i in range(len(neurons_size) - 1):
            self.neuron_size[i] += 1

        if weights is None:
            self.weights = []
            for i in range(len(neurons_size) - 1):
                self.weights.append(
                    [[random.uniform(-1, 1) for x in range(neurons_size[i + 1])] for y in range(neurons_size[i])])
        else:
            self.weights = weights

    def out(self, inp):
        out = [inp + [1]]
        for i in range(1, len(self.weights) + 1):
            a = []
            for j in range(self.neuron_size[i]):
                s = sum([out[i - 1][k] * self.weights[i - 1][k][j] for k in range(self.neuron_size[i - 1])])
                a.append(activation(s))
            if i != len(self.weights):
                a += [1]
            out.append(a)
        return out

    def correct(self, inp, answer, learning_rate=0.1):
        out = self.out(inp)
        errors = [[answer[i] - out[-1][i] for i in range(len(out[-1]))]]

        for i in range(len(self.weights) - 1, 0, -1):
            a = []
            for j in range(self.neuron_size[i]):
                s = sum([errors[0][k] * self.weights[i][j][k] for k in range(self.neuron_size[i + 1])])
                a.append((1 - out[i][j] ** 2) * s)
            errors.insert(0, a)

        for i in range(len(self.weights)):
            for j in range(self.neuron_size[i]):
                for k in range(self.neuron_size[i + 1]):
                    self.weights[i][j][k] += learning_rate * errors[i][k] * out[i][j]

        error_count = sum([sum(abs(en) for en in el) for el in errors])
        return out, error_count

    def mutate(self, mutate_k):
        for layer in range(len(self.weights)):
            for inp in range(len(self.weights[layer])):
                for outp in range(len(self.weights[layer][inp])):
                    self.weights[layer][inp][outp] += random.uniform(-mutate_k, mutate_k)

    def difference(self, other):
        if self.neuron_size != other.neuron_size:
            return None
        difference_count = 0
        for layer in range(len(self.weights)):
            for inp in range(len(self.weights[layer])):
                for outp in range(len(self.weights[layer][inp])):
                    difference_count += abs(self.weights[layer][inp][outp] - other.weights[layer][inp][outp])

        return difference_count

    def save(self, name):
        with open(name, 'w') as f:
            neuron_size = copy(self.neuron_size)
            for i in range(len(neuron_size) - 1):
                neuron_size[i] -= 1
            f.write(json.dumps({'shape': neuron_size, 'weights': self.weights}))

    def open(name):
        with open(name, 'r') as f:
            data = json.loads(f.read())
            return NeuralNetwork(data['shape'], data['weights'])

    def show(self, name):
        import matplotlib.pyplot as plt
        import networkx as nx
        from networkx.drawing.nx_agraph import graphviz_layout

        G = nx.DiGraph()

        for layer in range(len(self.neuron_size)):
            for neuron in range(self.neuron_size[layer]):
                G.add_node((layer, neuron))

        for layer in range(len(self.neuron_size) - 1):
            for from_neuron in range(self.neuron_size[layer]):
                for to_neuron in range(self.neuron_size[layer + 1]):
                    weight = self.weights[layer][from_neuron][to_neuron]
                    G.add_edge((layer, from_neuron), (layer + 1, to_neuron), weight=weight)

        pos = graphviz_layout(G, prog='dot', args="-Grankdir=LR")

        edge_widths = [2 + abs(G.edges[edge]['weight']) for edge in G.edges]
        edge_alpha = [abs(activation(G.edges[edge]['weight'])) / 2 for edge in G.edges]
        edge_colors = ['green' if G.edges[edge]['weight'] >= 0 else 'red' for edge in G.edges]

        nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue', alpha=0.8)

        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=edge_alpha, edge_color=edge_colors, arrows=True)

        layer_labels = {}
        for layer in range(len(self.neuron_size)):
            for neuron in range(self.neuron_size[layer]):
                layer_labels[(layer, neuron)] = f"{neuron}"
        nx.draw_networkx_labels(G, pos, labels=layer_labels, font_size=12, font_color='r')

        plt.axis('off')
        plt.title(f"Neural Network Weights")
        plt.savefig(f'{name}.png')

#!/usr/bin/python3

import networkx as nx
from matplotlib import pyplot as plt
import queue
import graphviz
import copy
import os

EPS = 'ε'

class Node:
    def __init__(self, label: str, mp: dict(), rmp: dict()):
        self.label = label
        if mp.__contains__(label):
            self.id = mp[label]
        else:
            self.id = mp.__len__()
            mp[self.label] = self.id
            rmp[self.id] = self.label

    def __str__(self):
        return self.label


class FiniteAutomata:

    def __init__(self, simga: frozenset):
        self.G = nx.MultiDiGraph()
        self.init_state = []
        self.final_state = []
        self.sigma = simga

    def add_node(self, label: str):
        self.G.add_node(label)

    def set_final_state(self, label: str):
        self.final_state.append(label)

    def set_final_state_from(self, labels: list):
        self.final_state += labels
        pass

    def set_init_state(self, label: str):
        self.init_state.append(label)

    def set_init_state_from(self, labels: list):
        self.init_state += labels
        pass

    def add_nodes_from(self, labels: list):
        self.G.add_nodes_from(labels)

    def add_edge(self, u: str, v: str, label=EPS):
        self.G.add_edge(u, v, key=label, label=label)

    def draw(self):
        f = graphviz.Digraph('finite state machine', filename='a.dot')
        f.attr(rankdir='LR', size='8,5')

        f.attr('node', shape='plaintext')
        f.node('start')

        f.attr('node', shape='doublecircle')
        for label in self.init_state:
            f.edge('start', str(label))
            f.node(str(label))
        for label in self.final_state:
            f.node(str(label))
        
        f.attr('node', shape='circle')
        for e in self.G.edges:
            print(e[0], e[1], e[2])
            u = str(e[0])
            v = str(e[1])
            f.edge(u, v, label=e[2])
        
        f.view()


    def draw_graphviz(self, png_path='./a.png', dot_file_path='./a.dot'):
        self.G.graph['edge'] = {'splines': 'curved'}
        A = nx.nx_pydot.to_pydot(self.G)
        A.write(dot_file_path)
        os.system("dot -Tpng {} > {}".format(dot_file_path, png_path))
        plt.imshow(plt.imread(png_path))
        plt.show()


    def eps_closure(self, l: list):
        q = queue.Queue()
        S = set()
        res = []
        for v in l:
            q.put(v)
            S.add(v)
        while not q.empty():
            u = q.get()
            res.append(u)
            for v in self.G[u]:
                if v in S:
                    continue
                if not EPS in self.G[u][v]:
                    continue
                q.put(v)
                S.add(v)

        return res

    def closure(self, l: list, label: str):
        l = self.eps_closure(l)
        S = set()
        res = []
        for u in l:
            for v in self.G[u]:
                if not v in S and label in self.G[u][v]:
                        S.add(v)
                        res.append(v)

        res = self.eps_closure(res)
        return res


def main():
    def testSimpletoDFA():

        f = FiniteAutomata(['0'])
        f.add_nodes_from(['A', 'B', 'C', 'D'])
        f.add_edge('A', 'B')
        f.add_edge('B', 'D')
        f.add_edge('B', 'C', '0')
        f.add_edge('C', 'D')
        f.add_edge('B', 'B', '0')
        # f.draw()
        f.draw_graphviz()
        # print(f.eps_closure(['A']))
        # print(f.closure(['A'], '0'))

    def testMulti():
        f = FiniteAutomata(['0', '1'])
        f.add_nodes_from(['A', 'B'])
        # f.add_edge('A', 'B', '0')
        # f.add_edge('A', 'B', '1')
        f.add_edge('A', 'B', '0')
        f.add_edge('A', 'B', '1')
        f.draw_graphviz()

    # testSimpletoDFA()
    testMulti()
    pass


if __name__ == "__main__":
    main()

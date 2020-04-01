#!/usr/bin/python3

import networkx as nx
from matplotlib import pyplot as plt
import queue, copy

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
            
    def __init__(self):
        self.G = nx.DiGraph()
        self.init_state = []
        self.final_state = []

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

    def add_edge(self, u: str, v: str, label='empty'):
        self.G.add_edge(u, v, weight=label)

    def draw(self):
        
        pos = nx.planar_layout(self.G)
        nx.draw(self.G, pos, with_labels=True)
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in self.G.edges(data=True)])
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
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
            # print(u)
            res.append(u)
            for v in self.G[u]:
                if (v in S) or (not self.G[u][v]['weight'] == 'empty'):
                    continue
                q.put(v)
                S.add(v)
                
        return res

    def closure(self, l: list, label: str):
        l = self.eps_closure(l)
        # q = queue.Queue()
        S = set()
        res = []
        for u in l:
            for v in self.G[u]:
                if not v in S and self.G[u][v]['weight'] == label:
                    S.add(v)
                    res.append(v)
        
        res = self.eps_closure(res)
        return res


def main():
    f = FiniteAutomata()
    f.add_nodes_from(['A', 'B', 'C', 'D'])
    f.add_edge('A', 'B')
    f.add_edge('B', 'D')
    f.add_edge('B', 'C', '0')
    f.add_edge('C', 'D')
    print(f.eps_closure(['A']))
    print(f.closure(['A'], '0'))
    pass

if __name__ == "__main__":
    main()

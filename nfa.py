#!/usr/bin/python3

import fa, dfa
class NFA(fa.FiniteAutomata):
    def toDFA(self):
        pass


if __name__ == '__main__':
    f = NFA()
    f.add_nodes_from(['A', 'B', 'C'])
    f.add_edge('A', 'B')
    l = f.eps_closure(['A'])
    print(l)
    f.draw()
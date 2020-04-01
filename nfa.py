#!/usr/bin/python3

import fa, dfa
import queue



class NFA(fa.FiniteAutomata):
    def toDFA(self):
        d = dfa.DFA(self.sigma)
        q = queue.Queue()

        mp = dict()
        f = frozenset(self.init_state)
        
        q.put(f)

        cnt = 0
        mp[f] = cnt
        d.add_node(cnt)
        cnt += 1
        d.set_init_state(0)
        
        while not q.empty():
            u = q.get()
            for w in self.sigma:
                v = self.closure(u, w)
                v = frozenset(v)
                if not v in mp:
                    mp[v] = cnt
                    d.add_node(cnt)
                    cnt += 1
                d.add_edge(mp[u], mp[v], w)

        return d


if __name__ == '__main__':
    n = NFA(['0'])

    n.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
    n.add_edge('A', 'B')
    n.add_edge('B', 'D')
    n.add_edge('B', 'C', '0')
    n.add_edge('C', 'E')
    n.set_init_state('A')
    n.add_edge('B', 'B', '0')

    print(n.eps_closure(['A']))
    print(n.eps_closure(['C']))

    d = n.toDFA()
    d.draw_graphviz()
import fa
from fa import EPS
class DFA(fa.FiniteAutomata):
    def addEdge(self, u: str, v: str, label=EPS):
        if label == EPS:
            raise Exception("epsilon is not allowed in dfa")
        super().add_edge(u, v, label)

    def __r_closure(self, l: frozenset, label: str):
        '''
very stupid implementation
        '''
        res = set()
        for label in self.G.nodes:
            flg = False
            for v in l:
                if v in self.G[label]:
                    flg = True
                    break

            if flg:
                res.add(label)
        return frozenset(res)
    
    def __hopcroft(self):
        Q = frozenset(self.G.nodes)
        F = frozenset(self.final_state)

        P = set([F, Q - F])
        W = set([F])

        while len(W) > 0:
            A = next(iter(W))
            W.remove(A)
            for c in self.sigma:
                X = self.__r_closure(A, c)
                if len(X) == 0:
                    continue
                l = []
                for Y in P:
                    sa = X & Y
                    sb = Y - X
                    if len(sa) == 0 or len(sb) == 0:
                        continue
                    l.append((Y, sa, sb))
                print(X)
                for Y, sa, sb in l:
                    print(Y, sa, sb)
                    P.remove(Y)
                    P.add(sa)
                    P.add(sb)
                    if Y in W:
                        W.remove(Y)
                        W.add(sa)
                        W.add(sb)
                    else:
                        if len(sa) <= len(sb):
                            W.add(sa)
                        else:
                            W.add(sb)
                # tmp = input()
        print(P)
        return P

    def minimize(self):
        d = DFA(self.sigma)
        mp = dict()
        P = self.__hopcroft()
        cnt = 0
        for A in P:
            mp[A] = cnt
            cnt = cnt + 1
        d.G.add_nodes_from(range(cnt))
        S = set()
        mp2 = dict()
        for A in P:
            for label in A:
                mp2[label] = A
        for s in self.init_state:
            S.add(mp[mp2[s]])
        d.init_state = list(S)
        S = set()
        for s in self.final_state:
            S.add(mp[mp2[s]])
        d.final_state = list(S)

        for e in self.G.edges:
            u = mp[mp2[e[0]]]
            v = mp[mp2[e[1]]]
            print(u, v, e[2])
            d.addEdge(u, v, e[2])
        print(d.G.nodes)
        print(d.G.edges)

        return d
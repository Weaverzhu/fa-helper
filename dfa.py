import fa
from fa import EPS
class DFA(fa.FiniteAutomata):
    def addEdge(self, u: str, v: str, label=EPS):
        if label == EPS:
            raise Exception("epsilon is not allowed in dfa")
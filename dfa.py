import fa
class Dfa(fa.FiniteAutomata):
    def addEdge(u: str, v: str, label='empty'):
        if label == 'empty':
            raise Exception("epsilon is not allowed in dfa")
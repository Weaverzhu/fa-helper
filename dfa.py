import fa
class DFA(fa.FiniteAutomata):
    def addEdge(u: str, v: str, label='empty'):
        if label == 'empty':
            raise Exception("epsilon is not allowed in dfa")
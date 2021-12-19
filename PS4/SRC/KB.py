from Literal import Literal


class KB():
    def __init__(self, _clauses):
        self.clauses = []
        for clause in _clauses:
            self.clauses.append([Literal(item) for item in clause])

    def clear(self):
        self.clauses = []
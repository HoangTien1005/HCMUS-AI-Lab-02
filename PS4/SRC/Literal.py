class Literal:
    def __init__(self, str_input):
        self.isnegative = False
        if str_input[0] == "-":
            self.isnegative = True
            self.name = str_input[1:]
        else:
            self.isnegative = False
            self.name = str_input[:]
    
    def negative(self):
        if self.isnegative:
            return Literal(self.name)
        else:
            return Literal("-" + self.name)

    def to_string(self):
        if not self.isnegative:
            return self.name
        else:
            return "-" + self.name

    def greater_than(self, other):
        return self.name > other.name
            
    def __eq__(self, other):
        return self.isnegative == other.isnegative and self.name == other.name

    def __hash__(self):
        return hash(self.to_string())

    def __repr__(self):
        return self.to_string()
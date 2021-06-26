class Vertex():
    """
    Define um vértice de um polígono, um ponto no R2.
    """
    def __init__(self, *args):
        self.x, self.y = args
        self.opposite_triangle = None
        self.boundary_chain = ""

    def __str__(self):
        return "%s %s" % (self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        """
        Retorna se self é "maior" que other
        de acordo com a ordenação topológica
        definida no livro do Berg.
        """
        if self.y > other.y:
            return True
        if other.y > self.y:
            return False
        return bool(self.x < other.x)
   
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    
    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

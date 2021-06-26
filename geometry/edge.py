def det(v_i, v_j):
    """
    Calcula o determinante de uma matriz 2x2
    |  v_i.x   v_j.x  |
    |  v_i.y   v_j.y  |
    """
    return (v_i[0] * v_j[1]) - (v_j[0] * v_i[1])


class HalfEdge():
    """
    Define um lado de uma aresta de um poligono
    representado por uma DoublyConnectedEdgeList.
    """
    def __init__(self, *args):
        self.orig, self.dest = args
        self.next = None
        self.prev = None

    def __str__(self):
        return "[%s] -> [%s]" % (self.orig,  self.dest)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.orig == other.orig and self.dest == other.dest

    def getOriginVector(self):
        """
        Retorna o vetor centrado na origem definido por sel.dest - self.orig
        """
        return self.dest - self.orig
        
    def setNext(self, next_half_edge):
        """
        Setter para a próxima half edge da lista de arestas.
        """
        self.next = next_half_edge

    def setPrev(self, prev_half_edge):
        """
        Setter para a half edge anterior na lista de arestas.
        """
        self.prev = prev_half_edge
    
    def goesToLeft(self):
        """
        Retorna True se a aresta vai para direita e falso se não.
        """
        vector = self.getOriginVector()
        j_hat = (0, 1)
        determinant = det(vector, j_hat) 
        return bool(determinant < 0)


class Edge():
    """
    Define uma aresta de uma DoublyConnectedEdgeList.
    """
    def __init__(self, *args, edge_type="boundary"):
        v_i, v_j,  = args
        self.half1 = HalfEdge(v_i, v_j)
        self.half2 = HalfEdge(v_j, v_i)
        self.next = None
        self.prev = None
        self.edge_type = edge_type

    def __str__(self):
        return str(self.half1)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.half1 == other.half1 and self.half2 == other.half2

    def setNext(self, edge):
        """
        Setter para a próxima half edge da lista de arestas.
        """
        self.half1.setNext(edge.half1)
        self.half2.setNext(edge.half2)
        self.next = edge

    def setPrev(self, edge):
        """
        Setter para a half edge anterior na lista de arestas.
        """
        self.half1.setPrev(edge.half1)
        self.half2.setPrev(edge.half2)
        self.prev = edge

    @staticmethod
    def filter(t): 
        return lambda e: e.edge_type == t

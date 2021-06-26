import sys
from geometry.vertex import Vertex
from geometry.edge import Edge

class Stack():
    """
    Define uma pilha auxiliar.
    """
    def __init__(self):
        self.vertices = []

    def __len__(self):
        return len(self.vertices)

    def top(self):
        """
        Retorna topo da pilha ou None se a pilha estiver vazia.
        """
        top = self.vertices[-1] if len(self.vertices) > 0 else None
        return top
        
    def pop(self):
        """
        Remove e retorna o vértice no topo da pilha ou None, se estiver vazia.
        """
        popped = self.vertices.pop(-1) if len(self.vertices) > 0 else None 
        return popped
        
    def popAll(self):
        """
        Remove e retorna todos os elementos da pilha ou None.
        """
        popped = []
        while len(self.vertices) != 0:
            popped.append(self.pop())
        return popped if len(popped) > 0 else None

    def push(self, v):
        """
        Empilha "v".
        """
        if v is not None:
            self.vertices.append(v)


class EventQueue():
    """
    Define uma fila de eventos.
    """
    def __init__(self, events):
        self.events = events

    def __len__(self):
        return len(self.events)
        
    def __getitem__(self, indx):
        return self.events[indx]
        
    def pop(self, e=None):
        """
        Remove o evento "e" se ele estiver na fila e o retorna,
        se "e" for None, remove e retorna o primeiro evento da fila,
        se a fila estiver vazia ou "e" não existir na fila, retorna None.
        """
        return self.events.pop(0) if e is None else self.events.pop(self.events.index(e))


class DoublyConnectedEdgeList():
    """
    Estrutura de dados para representar uma subdivisão do R2.
    """
    def __init__(self):
        self.vertices = []
        self.edges = []

    def __str__(self):
        string = ""
        string += (str(len(self.vertices)) + "\n")
        v = self.sortVertices()
        edge = self.getIncidentEdge(v[0])
        while edge.half1.next.orig != v[0]:
            string += (str(edge) + "\n")
            edge = edge.next
        string += str(edge.half1)
        return string
       
    def read(self):
        """
        Lê um polígono da entrada padrão
        """
        n_vertices = int(sys.stdin.readline())
        vertices = []
        orig_vertex = None
        edge = None
        prev_edge = None   
        for idx in range(0, n_vertices):
            dest_vertex = self.addVertex(*tuple(map(int, sys.stdin.readline().split(' '))))
            if orig_vertex is not None:
                edge = self.addEdge(orig_vertex, dest_vertex)
            if prev_edge is not None:
                edge.setPrev(prev_edge)
                prev_edge.setNext(edge)
            orig_vertex = dest_vertex
            prev_edge = edge      
        edge = self.addEdge(self.vertices[-1], self.vertices[0])
        edge.setPrev(prev_edge)
        prev_edge.setNext(edge)
        edge.setNext(self.edges[0])
        self.edges[0].setPrev(edge)

    def addVertex(self, *args):
        """
        Adiciona um vértice ao poligono.
        """
        self.vertices.append(Vertex(*args))
        return self.vertices[-1]
        
    def sortVertices(self):
        """
        Retorna uma lista de vertices
        ordenados topologicamente.
        (O vertice mais alto e mais a esquerda primeiro)
        """
        return sorted(self.vertices, reverse=True)
    
    def addEdge(self, *args, edge_type="boundary"):
        """
        Adiciona uma aresta ao poligono.
        """
        self.edges.append(Edge(*args, edge_type=edge_type))
        return self.edges[-1]

    def getIncidentEdge(self, orig):
        """
        Retorna edge que tem orig como vertice de origem da half_edge 1.
        """
        for e in filter(Edge.filter("boundary"), self.edges):
            if (e.half1.orig == orig):
                return e

from utils.datastruct import DoublyConnectedEdgeList
from .edge import HalfEdge

def det(v_i, v_j):
    """
    Calcula o determinante de uma matriz 2x2
    |  v_i.x   v_j.x  |
    |  v_i.y   v_j.y  |
    """
    return (v_i[0] * v_j[1]) - (v_j[0] * v_i[1])

def is_counter_clockwise(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


class Triangle():
    def __init__(self, vertices):
        v_0 , v_1, v_2 = tuple(sorted(vertices))
        if is_counter_clockwise(v_0, v_1, v_2):
            self.vertices = [v_0, v_2, v_1]
        self.vertices = [v_0, v_1, v_2]

    def __str__(self, polygon_vertices=None):
        v_0 , v_1, v_2 = tuple(self.vertices)
        if polygon_vertices is not None:
            return "%d %d %d" % (polygon_vertices.index(v_0)+1, polygon_vertices.index(v_1)+1, polygon_vertices.index(v_2)+1)
        return str([v_0, v_1, v_2])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        is_equal = True
        for v in self.vertices:
            is_equal = is_equal and v in other.vertices
        return is_equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_adjacent_triangles(self, triangles):
        adjacent_triangles = []
        for idx, v in enumerate(self.vertices):
            opposite_triangle = [t for t in triangles if self != t and self.vertices[(idx+1) % 3] in t.vertices and self.vertices[(idx+2) % 3] in t.vertices]
            adjacent_triangles += opposite_triangle if len(opposite_triangle) > 0 else [None]

        return "%d %d %d" % tuple([triangles.index(t)+1 if t is not None else 0 for t in adjacent_triangles])


class Polygon(DoublyConnectedEdgeList):
    """
    Subclasse de DoublyConnectedEdgeList que representa um poligono.
    """
    def __init__(self):
        self.triangles = []
        super(Polygon, self).__init__()
        
    def __str__(self):
        string = str(len(self.vertices))
        for vertex in self.vertices:
            string += "\n"
            string += str(vertex)
        return string

    def toString(self):
        string = ""
        string += str(len(self.triangles)) + "\n"
        for triangle in self.triangles:
            string += triangle.__str__(self.vertices) + " " + triangle.get_adjacent_triangles(self.triangles) + "\n"
        return string

    def getBoundaries(self):
        """
        Retorna uma tupla com duas listas de vertices,
        a cadeia de vertíces à esquerda e à direita do polígono.
        
        O vértice mais alto e o vertice mais baixo são omitidos
        """
        left_boundary = []
        right_boundary = []

        v = self.sortVertices()
        highest_v = v[0]
        lowest_v = v[-1]
        edge = self.getIncidentEdge(highest_v)

        if edge.half1.goesToLeft():
            aux_edge = edge.half1.next
            while aux_edge.orig != lowest_v:
                left_boundary.append(aux_edge.orig)
                aux_edge = aux_edge.next
            aux_edge = aux_edge.next
            while aux_edge.orig != highest_v:
                right_boundary.append(aux_edge.orig)
                aux_edge = aux_edge.next
        else:
            aux_edge = edge.half1.next
            while aux_edge.orig != lowest_v:
                right_boundary.append(aux_edge.orig)
                aux_edge = aux_edge.next
            aux_edge = aux_edge.next
            while aux_edge.orig != highest_v:
                left_boundary.append(aux_edge.orig)
                aux_edge = aux_edge.next
        
        return (left_boundary, right_boundary)

    def setBoundaries(self):
        """
        Seta o campo boundary de um vertice
        O vértice mais alto e o vertice mais baixo recebem highest e lowest, respectivamente.
        """
        left_boundary, right_boundary = self.getBoundaries()
        vertices = self.sortVertices()
        vertices[0].boundary_chain = "highest"
        vertices[-1].boundary_chain = "lowest"
        for v in vertices[1:len(vertices)-1]:
            if v in left_boundary:
                v.boundary_chain = "left"
            else:
                v.boundary_chain = "right"

    def addTriangle(self, v_1, v_2, v_3):
        self.triangles.append(Triangle(sorted([v_1, v_2, v_3])))

    def addDiagonal(self, orig, dest, test_vertex=None):
        """
        Adiciona uma diagonal no poligono se ela ficar contida nele.
        """
        if orig is None or dest is None:
            return None

        if test_vertex is not None:
            if orig.boundary_chain == "lowest":
                if dest.boundary_chain == "left":
                    v_i = HalfEdge(orig, dest).getOriginVector()
                    v_j = HalfEdge(orig, test_vertex).getOriginVector()
                else:
                    v_i = HalfEdge(orig, test_vertex).getOriginVector()
                    v_j = HalfEdge(orig, dest).getOriginVector()
                
            elif dest.boundary_chain == "highest":
                if orig.boundary_chain == "left":
                    v_i = HalfEdge(orig, dest).getOriginVector()
                    v_j = HalfEdge(orig, test_vertex).getOriginVector()
                else:
                    v_i = HalfEdge(orig, test_vertex).getOriginVector()
                    v_j = HalfEdge(orig, dest).getOriginVector()

            else:
                if orig.boundary_chain == "left":
                    v_i = HalfEdge(orig, dest).getOriginVector()
                    v_j = HalfEdge(orig, test_vertex).getOriginVector()
                else:
                    v_i = HalfEdge(orig, test_vertex).getOriginVector()
                    v_j = HalfEdge(orig, dest).getOriginVector()
            
            if det(v_i, v_j) <= 0:
                return None

        
        diagonal = self.addEdge(orig, dest, edge_type="diagonal")
        
        return diagonal

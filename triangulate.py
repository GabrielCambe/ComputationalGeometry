#!/usr/bin/env python3
# -- coding: utf-8 --

"""
    USO:
    Para triangular um poligono especificado or um arquivo, faça:
    $ python3 triangulate.py < arquivo
        
    Se você tiver executado make antes, pode fazer:
    $ ./triangulate.py < arquivo
"""

import sys
from utils.datastruct import EventQueue, Stack
from geometry.polygon import Polygon 
from geometry.edge import Edge 


def makeMonotone(P):
    """
    """
    return [P]


def triangulateMonotonePolygon(P):
    """
    Entrada: Um poligono P, estritamente y-monótono
    Saída: Uma triangulação de P.
    """
    Q = EventQueue(P.sortVertices())
    P.setBoundaries()
    S = Stack()
    S.push(Q[0])
    S.push(Q[1])
    for i in range(2, len(Q)-1):
        if Q[i].boundary_chain != S.top().boundary_chain:
            vertices = S.popAll()
            for idx, vertex in enumerate(vertices):
                if idx != len(vertices)-1:
                    if P.addDiagonal(Q[i], vertex, Q[i+1] if (Q[i+1].y == Q[i].y) and (Q[i+1].boundary_chain == Q[i].boundary_chain) else None) is not None:
                        P.addTriangle(Q[i], vertex, vertices[idx+1])
                
            S.push(Q[i-1])
            S.push(Q[i])
        else:
            popped_vertex = S.pop()
            while P.addDiagonal(Q[i], S.top(), popped_vertex) is not None:
                previous_popped_vertex = popped_vertex
                popped_vertex = S.pop()
                P.addTriangle(Q[i], popped_vertex, previous_popped_vertex)
            S.push(popped_vertex)
            S.push(Q[i])

    if len(S) > 2:
        for vertex in S.vertices[1:len(S)-1]:
            P.addDiagonal(Q[len(Q)-1], vertex)
    else:
        P.addTriangle(Q[len(Q)-1], S.vertices[len(S)-1], S.vertices[0])
    
    return P


def triangulateSimplePolygon(P):
    """
    Entrada: Um polígono simples P.
    Saída: Uma triangulação do polígono P.
    """
    monotone_polygons = makeMonotone(P)
    trngltn = [triangulateMonotonePolygon(plgn) for plgn in monotone_polygons]
    return trngltn[0]


polygon = Polygon()
polygon.read()
print(polygon)
triangulation = triangulateSimplePolygon(polygon)
print(triangulation.toString())

sys.stderr.write("Diagonais adicionadas: " + str(list(filter(Edge.filter("diagonal"), triangulation.edges)))+ "\n\n")

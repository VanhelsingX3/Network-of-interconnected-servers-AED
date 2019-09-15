from recursiveJson import *

class Vertex:
    def __init__(self,name):
        self.name = name
        self.edges = {}
        self.valueToEdges = {}
    
    def addEdge(self,node,weight = 1):
        self.edges[node] = node.valueToEdges

    def addCharacteristics(self,distance,bandwidth,usersOnline,traffic,meanType):
        self.valueToEdges["Distancia"] = distance
        self.valueToEdges["Ancho de banda"] = bandwidth
        self.valueToEdges["Cantidad de usuarios"] = usersOnline
        self.valueToEdges["Cantidad de trafico"] = traffic
        self.valueToEdges["Tipo de medio"] = meanType


class Graph:
    def __init__(self):
        self.vertices = {}

    def addVertex(self,vertex):
        self.vertices["%s" % (vertex.name)] = vertex.edges



#=============================  M A I N ============================
"""
grafo = Graph()
vertex1 = Vertex("Servidor A")
vertex1.addCharacteristics(10,100,2,60,'Coaxcial')

vertex2 = Vertex("Servidor B")
vertex2.addCharacteristics(21,200,4,120,'CAT5')

vertex3 = Vertex("Servidor C")
vertex3.addCharacteristics(30,300,6,180,'Wifi')

vertex4 = Vertex("Servidor D")
vertex4.addCharacteristics(60,400,8,240,'Fibra Optica')


vertex1.addEdge(vertex2)
vertex1.addEdge(vertex3)

vertex2.addEdge(vertex4)
vertex2.addEdge(vertex1)
vertex2.addEdge(vertex3)

#vertex3.addEdge(vertex4)
vertex3.addEdge(vertex1)
vertex3.addEdge(vertex2)

#vertex4.addEdge(vertex3)
#vertex4.addEdge(vertex2)

grafo.addVertex(vertex1)
grafo.addVertex(vertex2)
grafo.addVertex(vertex3)
grafo.addVertex(vertex4)

json = grafo.vertices

#print("Hola")
ConvertDictToText = ConvertDictToText()
ConvertDictToText.convert(json)
"""

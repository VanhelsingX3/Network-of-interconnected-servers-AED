from recursiveJson import *
class Vertex:
	def __init__(self,name):
		self.name = name
		self.edges ={}
		self.weight = None

	def addEdge(self,node,distance,bandwidth,usersOnline,traffic,meanType):
		self.edges[node.name] = self.getWeight(distance,bandwidth,usersOnline,traffic,meanType)


	#Retortnar el peso.
	def getWeight(self,distance,bandwidth,usersOnline,traffic,meanType):
		return 10


				

#Clase para gestion de los vertices en el grafo.
class Graph:
	def __init__(self):
		self.vertices = {}										#{A:{B:10}}

	def addVertex(self,vertex):
		self.vertices["%s" % (vertex.name)] = vertex.edges

	def printGraph(self):
		graf = self.vertices
		for k,v in graf.items():
			#print("Vertice:%s" % k)
			for aris,w in v.items():
				print("Vertice:%s\tArista:%s - peso:%s" % (k,aris,w)) 
"""
graf = Graph()
vertexA = Vertex("A")
vertexB = Vertex("B")
vertexA.addEdge(vertexB,100,50,5,70,"Wifi")
vertexB.addEdge(vertexA,100,50,5,70,"Wifi")
graf.addVertex(vertexA)
graf.addVertex(vertexB)
graf.printGraph()
"""







#-------------------------------------------------------------------------------------------------------------------
#Clase para encontrar las rutas de un grafo.
class BuildPaths:
	def __init__(self):
		self.stack = []
		self.paths = []

	#Encuentra y guarda TODAS las rutas entre un vertice origen, a un destino.
	def findPaths(self,start,destination,dict):
		self.stack.append([start])                                   #Agrega el vertice inicio.
		while self.stack:                                            #Mientras la cola tenga valores.
			tempPath = self.stack.pop()                              #Extra el ultimo indice de la lista.
			key = tempPath[-1]                                       #Extrae el ultimo valor del elemento.
			for i in self.subtractLists(dict[key],tempPath):         #Llama a la funcion que 'resta' los elementos de las listas dadas, devolviendo otra lista.
				if i == destination:                                 #Stop si el valor de la 'resta' es el destino deseado.
					self.paths.append(tempPath + [i])                #Se agrega a la variable de rutas.
				else:
					self.stack.append(tempPath + [i])                #En caso que no sea el valor destino, se sigue agregando rutas, volviendo al while.

	#'Resta' los valores de las listas dadas.
	#ejm: ['A','B','C'] - ['A','C'] = ['B']
	def subtractLists(self,listaA,listaB):
		listTemp = []
		for i in listaA:
			if i in listaB:
				pass
			else:
				listTemp.append(i)
		return listTemp
	
	def getPaths(self):
		return self.paths

#vertexA = Vertex("A")
#vertexA.addCharacteristics("10","50","5","200","Wifi")
#vertexA.getWeight()
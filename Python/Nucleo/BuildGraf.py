#Clase para los vertices.
class Vertex:
	def __init__(self,name):
		self.name = name
		self.edges ={}
		self.weight = 10

	#Utilizada para agregar una arista a un vertices, recibiendo sus caracteristicas.
	def addEdge(self,node,distance,bandwidth,usersOnline,traffic,meanType):
		self.edges[node.name] = self.getWeight(distance,bandwidth,usersOnline,traffic,meanType)						

	#Retortnar el peso calculado.
	def getWeight(self,distance,bandwidth,usersOnline,traffic,meanType):
		return self.weight


#Clase para gestion de los vertices en el grafo.
class Graph:
	def __init__(self):
		self.vertices = {}										#{A:{B:10}}

	#Agregar vertice.
	def addVertex(self,vertex):
		self.vertices["%s" % (vertex.name)] = vertex.edges

	#imrpimir el grafo.
	def printGraph(self):
		graf = self.vertices
		for k,v in graf.items():
			for aris,w in v.items():
				print("Vertice:%s\tArista:%s - peso:%s" % (k,aris,w)) 

	#Busca el peso entre un Vertice y Otro.
	def searchEdgeWeight(self,nameVertex1,nameVertex2):
		for k,v in self.vertices.items():					#k = str, v = dict
			if(k == nameVertex1):
				for aris,w in v.items():
					if(aris == nameVertex2):						
						#print("k:%s aris:%s - w:%s" %(k,aris,w))
						return w						#Retorna el peso entre las aristas.

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
			#print(dict[key][0][0])
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
			#print(i[0])
			if i[0] in listaB:
				pass
			else:
				listTemp.append(i[0])
		#print(listTemp)
		return listTemp
	
	def getPaths(self):
		return self.paths

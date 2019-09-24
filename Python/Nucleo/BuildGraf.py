# -*- coding: utf-8 -*-
#Clase para los vertices.
class Vertex:
	def __init__(self,name):
		self.name = name
		self.edges ={}
		self.weight = None

	#Utilizada para agregar una arista a un vertices, recibiendo sus caracteristicas.
	def addEdge(self,node,distance,bandwidth,usersOnline,traffic,meanType):
		self.edges[node.name] = self.getWeight(distance,bandwidth,usersOnline,traffic,meanType)						
	
	#Retortnar el peso calculado.
	def getWeight(self,distance,bandwidth,usersOnline,traffic,meanType):
		subTotalForDistance = self.decreaseInReliability(distance,meanType)
		subtTotalForBandwidth = self.calculateForBandwidth(bandwidth,usersOnline,traffic)
		totalReliabilty = subTotalForDistance + subtTotalForBandwidth
		if(totalReliabilty < 0):
			totalReliabilty = 0
		if(totalReliabilty > 1):
			totalReliabilty = 1

		totalReliabilty = "{0:.2f}".format(totalReliabilty)
		self.weight = totalReliabilty
		return float(self.weight)

	def decreaseInReliability(self,distance,meanType):
		reliability = None
		partition = None
		if(meanType == 'CAT5'):
			reliability = 0.98
			decrease = 0.02					#Disminucion de confiabilidad%
			partition = 50 					#Cada partition metros 			
		if(meanType == 'CAT6'):
			reliability = 0.98
			decrease = 0.01
			partition =	50	
		if(meanType == 'Fibra-Optica' or meanType == 'Fibra-Óptica'):
			reliability = 0.90
			decrease = 0.05		
			partition =	100	
		if(meanType == 'Wifi' or meanType == "WIFI"):
			reliability = 0.7
			decrease = 0.06		
			partition =	6	
		if(meanType == 'Coaxial'):
			reliability = 1
			decrease = 0.04		
			partition =	100	
		if(meanType == 'Par-Trenzado'):	
			reliability = 1
			decrease = 0.01		
			partition = 100
		
		subTotalForDistance = (int(distance)/partition)*decrease
		totalDistanceDecrease = reliability - subTotalForDistance
		return totalDistanceDecrease

	def calculateForBandwidth(self,bandwidth,usersOnline,traffic):
		bandwidth = int(bandwidth)
		usersOnline = int(usersOnline)
		traffic = int(traffic)
		subtTotalForBandwidth = (traffic - bandwidth)/usersOnline						#mbps
		percentage = (subtTotalForBandwidth/bandwidth)*100
		reliability = 0
		if(percentage >=1 and percentage < 25):
			reliability = 0.05
		if(percentage >=25 and percentage < 50):
			reliability = 0.10
		if(percentage >=50 and percentage < 75):
			reliability = 0.15
		if(percentage >= 75 and percentage <=100):
			reliability = 0.20
		if(percentage < 1):
			reliability = 0
		return reliability	


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
		return listTemp
	
	def getPaths(self):
		return self.paths

# -*- coding: utf-8 -*-
from recursiveJson import *
from LinkedList import *
from BuildGraf import *
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import PyQt5.QtCore as core
import sys
import networkx as nx 
import matplotlib.pyplot as plt 

class PWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = "Ventana Principal"
		self.setGeometry(0,0,450,550)					
		#QMainWindow.setWindowFlags(self, core.Qt.FramelessWindowHint)
		self.boxsText()
		self.buttons()
		
		self.layoutPWindow()

		css = """
		QMainWindow{
	  	background-color: lightblue;
	  	color:black;
		"""

		#self.setStyleSheet(css)
		self.centerWindow()

	def boxsText(self):
		self.boxOfCharacteristics = QTextEdit(self)
		#self.boxOfCharacteristics.setText("Hola")
		#self.boxOfCharacteristics.setPlaceholderText("Origin Node")
		#self.boxOfCharacteristics.resize(100,40)

		self.boxOfOrigin = QLineEdit(self)
		self.boxOfOrigin.setPlaceholderText("Nodo origen")
		self.boxOfOrigin.resize(20,10)

		self.boxOfDestiny = QLineEdit(self)
		self.boxOfDestiny.setPlaceholderText("Nodo Destino")
		self.boxOfDestiny.resize(20,10)

	def buttons(self):
		self.btnFileUpload = QPushButton("Cargar archivo")
		self.btnFileUpload.setToolTip("Carga un archivo para crear un mapa")
		self.btnFileUpload.clicked.connect(self.enableButtonUpload)

		self.btnCreateMap = QPushButton("Crear mapa")
		self.btnCreateMap.setToolTip("Carga un archivo para crear un mapa")
		self.btnCreateMap.clicked.connect(self.enableCreateMap)
		
		self.btnCreateTable = QPushButton("Crear tabla")
		self.btnCreateTable.setToolTip("Crear tabla con la informacion dada")
	
	def layoutPWindow(self):
		self.hBoxCharacteristicsLayout = QHBoxLayout()
		self.hBoxCharacteristicsLayout.addWidget(self.boxOfCharacteristics)

		self.hBoxOriginAndDestinyLayout = QHBoxLayout()
		self.hBoxOriginAndDestinyLayout.addWidget(self.boxOfOrigin)
		self.hBoxOriginAndDestinyLayout.addWidget(self.boxOfDestiny)

		self.hButtonsUploadAndCreateMapLayout = QHBoxLayout()
		self.hButtonsUploadAndCreateMapLayout.addWidget(self.btnFileUpload)
		self.hButtonsUploadAndCreateMapLayout.addWidget(self.btnCreateMap)

		self.hButtonCreateTableLayout = QHBoxLayout()
		self.hButtonCreateTableLayout.addWidget(self.btnCreateTable)

		self.vFinalLayout = QVBoxLayout()
		self.vFinalLayout.addLayout(self.hBoxCharacteristicsLayout)
		self.vFinalLayout.addLayout(self.hBoxOriginAndDestinyLayout)
		self.vFinalLayout.addLayout(self.hButtonsUploadAndCreateMapLayout)
		self.vFinalLayout.addLayout(self.hButtonCreateTableLayout)

		self.orderingLayout = QWidget()
		self.orderingLayout.setLayout(self.vFinalLayout)
		self.setCentralWidget(self.orderingLayout)

#-----------------FUNCIONES A LOS WIDGET DE LA VENTANA------------------
	def enableCreateMap(self):
		convertDictToText = ConvertDictToText()
		G = nx.DiGraph()

		textOfBoxOfCharacteristics = self.boxOfCharacteristics.toPlainText()
		textOfBoxOfCharacteristics = textOfBoxOfCharacteristics.split('\n')	
		
		LLOfVertex = self.extractValuesToTextFormat(textOfBoxOfCharacteristics)		
		objectGraph = self.convertLLInDict(LLOfVertex)

		g = objectGraph.vertices
		for k,v in g.items():
			G.add_node(str(k))
			for edge in v:
				G.add_node(str(edge.name))
				G.add_edge(str(k), str(edge.name), weight=1)
		#convertDictToText.convert(objectGraph.vertices,"PruebaJsonWithDict.txt")
		pos = nx.spring_layout(G)
		nx.draw(G,rows=True, with_labels=True,node_color='r',node_size=4000,edge_color='b',arrowsize=30)
		#plt.savefig("plot.png")
		plt.show()



		"""
#===========================GRAFICANDO SOLO CON LA LISTA ENLAZADA==============================================

		for i in range(LLOfVertex.length()):
			item = LLOfVertex.atPosition(i)
			G.add_node(str(item.name))
			for j in range(item.edges.length()):
				itemVertex = item.edges.atPosition(j)
				G.add_edge(str(item.name),str(itemVertex.name), weight=5)
		
		edg = [('Servidor A', 'Servidor C')]
		pos = nx.spring_layout(G)
		nx.draw(G,rows=True, with_labels=True,node_color='r',node_size=4000,edge_color='b',arrowsize=30)
		
		self.imageGraph = plt.savefig("plot.png")
		mapWindow = MapWindow()
		plt.show()
		"""		

	#Extrae todos los vertices,aristas y caracteristicas del contenido de la caja de texto guardandolos en una lista enlazada.
	def extractValuesToTextFormat(self,textOfBoxOfCharacteristics):	
		vertexLL = LinkedList()
		for i in range(len(textOfBoxOfCharacteristics)):						#Recorrera el contenido de la caja, para obtener los vetices.
			currentItem = textOfBoxOfCharacteristics[i]
			if(currentItem.find('\t') == -1):
				findItem = ("\t%s" % currentItem)
				if(findItem != '\t'):
					for j in range(len(textOfBoxOfCharacteristics)):
						currentItemSecundaryItem = textOfBoxOfCharacteristics[j]
						item = currentItemSecundaryItem.strip()
						if(currentItemSecundaryItem.find(findItem) != -1):
							name = item
							bandwidth = self.extractValueToString(textOfBoxOfCharacteristics[j+1])
							usersOnline = self.extractValueToString(textOfBoxOfCharacteristics[j+2])
							traffic	= self.extractValueToString(textOfBoxOfCharacteristics[j+3])
							distance = self.extractValueToString(textOfBoxOfCharacteristics[j+4])
							meanType = self.extractValueToString(textOfBoxOfCharacteristics[j+5])
							vertexLL.add(name,distance,bandwidth,usersOnline,traffic,meanType)
							#print("%s,%s,%s,%s,%s,%s" % (name,bandwidth,usersOnline,traffic,distance,meanType))
							break
		
		for k in range(len(textOfBoxOfCharacteristics)):						#Recorrera el contenido de la caja, para obtener las aristas.
			itemVertex = textOfBoxOfCharacteristics[k]
			if(itemVertex.find('\t') == -1):
				for m in range(len(textOfBoxOfCharacteristics)):
					if(textOfBoxOfCharacteristics[m] == itemVertex):
						#print("------------%s --------------" % itemVertex)
						index = m + 1
						if(index < len(textOfBoxOfCharacteristics)):
							while(textOfBoxOfCharacteristics[index].count('\t') >= 1):
								if(textOfBoxOfCharacteristics[index].count('\t') == 1):
									itemT = textOfBoxOfCharacteristics[index].strip()
									name = itemT
									bandwidth = self.extractValueToString(textOfBoxOfCharacteristics[index+1])
									usersOnline = self.extractValueToString(textOfBoxOfCharacteristics[index+2])
									traffic	= self.extractValueToString(textOfBoxOfCharacteristics[index+3])
									distance = self.extractValueToString(textOfBoxOfCharacteristics[index+4])
									meanType = self.extractValueToString(textOfBoxOfCharacteristics[index+5])									
									#print("%s,%s,%s,%s,%s,%s" % (name,bandwidth,usersOnline,traffic,distance,meanType))
									#print(name)
									vertexLL.searchInLL(itemVertex).edges.add(itemT,textOfBoxOfCharacteristics[m+1],None,None,None,None)
								index += 1
		return vertexLL
	
	#Convierte los datos extraidos del texto, a un diccionario, para luego crear el mapa.
	def convertLLInDict(self,LLOfVertex):
		graph = Graph()
		LLOfEdges = LinkedList()
		for i in range(LLOfVertex.length()):
			currentNode = LLOfVertex.atPosition(i)
			vertex = Vertex(currentNode.name)
			LLOfEdges.add(currentNode.name,vertex,None,None,None,None)					#Almacena los vertices 
			vertex.addCharacteristics(currentNode.distance,currentNode.bandwidth,currentNode.usersOnline,currentNode.traffic,currentNode.meanType)
			
		
		for j in range(LLOfEdges.length()):
			currentItem = LLOfEdges.atPosition(j)
			item = LLOfVertex.searchInLL(currentItem.name)								#Arista a agregar
			for k in range(item.edges.length()):
				currentEdge = item.edges.atPosition(k).name

				vertexToAdd = LLOfEdges.searchInLL(currentEdge).distance			#Aqui esta guardado la informacion de tipo VERTEX
				currentItem.distance.addEdge(vertexToAdd)
			graph.addVertex(currentItem.distance)
		return graph





	#Extrae el valor de una caracteristica(str). ej: Distancia:100 => 100
	def extractValueToString(self,string,toFind = ":"):
		indexFindChar = string.find(toFind)
		_len = len(string)
		newChar = string[indexFindChar+1 : _len]
		return newChar	
				
		
	def enableButtonUpload(self):
		filePath = QFileDialog.getOpenFileName(self, "Selecciona el archivo a cargar.")
		filePath = filePath[0]
		tempList = []
		
		f = open(filePath,"r")
		lineas = f.readlines()
		for i in lineas:
			tempList.append(i)
		f.close()
		self.content = "".join(tempList)
		self.boxOfCharacteristics.setText(self.content)
		
	def centerWindow(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move(size.width()*1.5,size.height())




class MapWindow(QDialog):
	def __init__(self, parent = None):
		QDialog.__init__(self, parent)
		label = QLabel(self)
		#pixmap = QPixmap('plot.png')
		#pixmap.scaled(20, 20)
		#label.setPixmap(pixmap)
		#self.resize(pixmap.width(),pixmap.height())



if __name__ == "__main__":
	app = QApplication(sys.argv)
	#app.setWindowIcon(QtGui.QIcon("images/icon_application.png"))

	window = PWindow()
	window.setWindowTitle("Mapa de grafos")

	window.show()
	sys.exit(app.exec_())
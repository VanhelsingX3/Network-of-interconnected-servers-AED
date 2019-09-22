# -*- coding: utf-8 -*-
#from recursiveJson import *
from LinkedList import *
from BuildGraf import *
from QuickSort import *
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

		self.objectGraph = None


		#self.openMapWindow()
		paint = """
		QMainWindow{
	  	background-color:skyblue;
	  	color:black;
	  	background-repeat:no-repeat;
		background-position:center top;
		}QPushButton{
			background-color: lightblue;
			color:black;
			border-style: solid;
			border-radius: 7;
			padding: 5px;
			padding-left: 7px;
			padding-right: 30px;
			border-color: black;
			border-width: 2px;
			font-family:Arial;
			font-size : 28

		}
		"""

		self.setStyleSheet(paint)
		self.centerWindow()

	#Define y establece las cajas de texto para la ruta origen y destino.
	def boxsText(self):
		self.boxOfCharacteristics = QTextEdit(self)
		#self.resize(550,450)
		self.boxOfOrigin = QLineEdit(self)
		self.boxOfOrigin.setPlaceholderText("Nodo origen")
		self.boxOfOrigin.setFixedSize(212,40)

		self.boxOfDestiny = QLineEdit(self)
		self.boxOfDestiny.setPlaceholderText("Nodo Destino")
		self.boxOfDestiny.setFixedSize(212,40)

		self.labelTextMessage = QLabel()
		self.labelTextMessage.setEnabled(False)

	#Creacion de los botones de la ventana.
	def buttons(self):
		self.btnFileUpload = QPushButton("Cargar archivo")
		self.btnFileUpload.setFixedSize(212,60)
		#self.btnFileUpload.bor
		self.btnFileUpload.setToolTip("Carga un archivo para crear un mapa")
		self.btnFileUpload.clicked.connect(self.enableButtonUpload)

		self.btnCreateMap = QPushButton("Crear mapa")
		self.btnCreateMap.setFixedSize(212,60)
		self.btnCreateMap.setToolTip("Carga un archivo para crear un mapa")
		self.btnCreateMap.clicked.connect(self.enableCreateMap)
		
		self.btnCreateTable = QPushButton("Crear tabla")
		self.btnCreateTable.setFixedSize(212,60)
		self.btnCreateTable.setToolTip("Crear tabla con la informacion dada")
		self.btnCreateTable.clicked.connect(self.enableButtonCreateTable)

	#Ordenamiento por cajas de los widgets.
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
		self.vFinalLayout.addWidget(self.labelTextMessage)
		self.vFinalLayout.addLayout(self.hBoxOriginAndDestinyLayout)
		self.vFinalLayout.addLayout(self.hButtonsUploadAndCreateMapLayout)
		self.vFinalLayout.addLayout(self.hButtonCreateTableLayout)

		self.orderingLayout = QWidget()
		self.orderingLayout.setLayout(self.vFinalLayout)
		self.setCentralWidget(self.orderingLayout)

#-----------------FUNCIONES GENERALES------------------
	#Funcion que se activa al presionar el boton de crear mapa.
	def enableCreateMap(self):
		G = nx.DiGraph()
		fig = plt.figure()
		self.enableLabel(False)
		
		#Recorre el diccionario creado del texto, extrayendo sus llaves,valores,peso para dibujar.
		if(self.objectGraph != None):
			g = self.objectGraph.vertices
			for k,v in g.items():
				for aris,w in v.items():
					G.add_node(str(k))
					G.add_edge(str(k), str(aris),weight=int(w),background_weight='black')

			#Establece y determina el dibujado utilizando 'nx'.
			pos = nx.spring_layout(G)
			nx.draw(G,pos,rows=True, with_labels=True,node_color='skyblue',node_shape="o",node_size=4000,edge_color='lightblue',arrowsize=20,font_color='white',style='dashed')		
			labels = nx.get_edge_attributes(G,'weight')
			nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_family='sans-serif')
			
			#fig.set_facecolor("#00000F")
			plt.savefig('graph.png') #facecolor=fig.get_facecolor() )				#Guarda la imagen dado una ruta.
			
			self.openMapWindow()													#Abre otra ventana para mostrar el mapa creado.
		else:
			self.enableLabel(True,"No hay un archivo cargado para dibujar el mapa.")

	#Carga el archivo de texto, y lo excribe en la caja de EditText
	def enableButtonUpload(self):
		filePath = QFileDialog.getOpenFileName(self, "Selecciona el archivo a cargar.")
		filePath = filePath[0]		
		if(filePath != ''):																#Si se ha elegido un archivo, caso contrario muestra un mensaje.
			tempList = self.extractContentToBoxOfCharacteristics(filePath)				#Guarda el contenido extraido del archivo cargado.
			self.content = "".join(tempList)											
			self.boxOfCharacteristics.setText(self.content)								#Traspasa el contenido cargado a la caja de texto.

			LLOfVertex = self.extractValuesToTextFormat()		
			self.objectGraph = self.convertLLInDict(LLOfVertex)							#La variable con el diccionario del contenido de la caja de texto.

	#Funcion que usa al presionar el boton crear tabla.
	def enableButtonCreateTable(self):
		newJson = {}
		buildPaths = BuildPaths()
		paths = None
		LLOfPathsAndWeigth = LinkedList()
		sort = QuickSort()																#Algoritmo de ordenamiemto, utilizado para ordenar ascendentemente los pesos de las rutas.
		arrWeight = []
		self.enableLabel(False)
		if(self.objectGraph != None):													#Si hay un diccionario, == None cuando no se ha cargado un archivo.
			jsonGraph = self.objectGraph.vertices
			
			for k,v in jsonGraph.items():												#Recorre el diccionario.
				newJson[k]=[]
				for aris,w in v.items():
					temp = []
					temp.append(aris)
					temp.append(w)
					newJson[k].append(temp)

			origin = self.boxOfOrigin.text()											#Extrae el texto de la caja origen.
			destination = self.boxOfDestiny.text()										#Extrae el texto de la caja destino.
			stateO,stateD = self.checkVertexExists(origin,destination,newJson)

			#------------Control del input del origen y dpyestino------------
			if(stateO == True and stateD == True):										#En caso que los valores de las cajas, existan en el diccionario.
				buildPaths.findPaths(origin,destination,newJson)						#Busca todas las rutas desde el punto origen, al destino.
				paths = buildPaths.getPaths()											#Devuelve y guarda las rutas encontradas.
				self.labelTextMessage.setVisible(False)

				title = ("%s\n%s%s%s\n%s\n" % ('='*78,'\t'*3,'T A B L A  D E  R U T A S','\t'*3,'='*78))
				titleSubTable = ("%s" % ('\tPeso\t|\tRuta\n'))
				dates = ""
				
				#Este ciclo recorrera todos las rutas, para guardarlas en una LL, para asi mas adelante poder ordenar las rutas desde el menor peso, al mayor peso...
				#...por el cual el primer o primeros elementos de la lista en tabla, sera la ruta mas corta.
				for i in paths:																					#Ruta de vertices
					weight = self.searchWeight(i,self.objectGraph)
					LLOfPathsAndWeigth.add(i,weight,None,None,None,None)										#name:ruta,distance:peso
					arrWeight.append(weight)
				
				sort.sort(arrWeight)
				tempPath = []
				for j in arrWeight:
					state = True
					for k in range(LLOfPathsAndWeigth.length()):
						currentNode = LLOfPathsAndWeigth.atPosition(k)
						if(j == currentNode.distance and currentNode.name not in tempPath and state == True):															#En el atributo distance esta guardado el peso.
							tempPath.append(currentNode.name)
							temp = ("%s\n\t%s\t|\t%s\n" % ('-'*139,j,",".join(currentNode.name)))
							dates = dates + temp
							state = False
						
				content = title + titleSubTable + dates															#Contiene todo el contenido a mostrar en la ventana de la tabla.
				self.openTableWindows(content)
			
			elif(stateO == True and stateD == False):
				self.enableLabel(True,'El valor destino no existe')
				print("True","False")
			
			elif(stateO == False and stateD == True):
				print("False,True")
				self.enableLabel(True,'El valor origen no existe')
			
			elif(stateO == False and stateD == False):
				self.enableLabel(True,'El valor origen y destino no existen')
				print("False,False")				
		else:
			self.enableLabel(True,"No hay un archivo cargado para obtener la tabla.")


	#Funcion que extrae el peso de las aristas, reciendo las rutas y el objeto grafo.
	def searchWeight(self,paths,jsonGraph):
		arrWeigth = []
		weigth = 0
		for i in range(len(paths)):
			index = i+1
			if(index < len(paths)):
				arrWeigth.append(jsonGraph.searchEdgeWeight(paths[i],paths[index]))
		for j in arrWeigth:
			weigth = weigth + j
		return weigth

	#-----------------------------FUNCIONES LLAMADAS POR LAS GENERALES----------------------------------------------
	#Esta funcion extrae todo el contenido del archivo seleccionado.	
	def extractContentToBoxOfCharacteristics(self,filePath):
		tempList = []
		f = open(filePath,"r")
		lineas = f.readlines()
		size = len(lineas)
		for i in range(len(lineas)):
			tempList.append(lineas[i])
			
			if(i == size-1):
				if(lineas[i] != '\n'):
					tempList.append('\n')
		f.close()
		return tempList

	#Revisa si los vertices existen en el diccionario dado.
	def checkVertexExists(self,origin,destination,json):
		tempArr = []
		for k in json.keys():
			tempArr.append(k)

		for i in tempArr:
			if(origin in tempArr and destination not in tempArr):						
				return True,False

			if(origin not in tempArr and destination in tempArr):
				return False,True
			
			if(origin not in tempArr and destination not in tempArr):
				return False,False

			if(origin in tempArr and destination in tempArr):
				return True,True

	#Extrae todos los vertices,aristas y caracteristicas del contenido de la caja de texto guardandolos en una lista enlazada.
	def extractValuesToTextFormat(self):	
		textOfBoxOfCharacteristics = self.boxOfCharacteristics.toPlainText()
		textOfBoxOfCharacteristics = textOfBoxOfCharacteristics.split('\n')
		vertexLL = LinkedList()
		for i in range(len(textOfBoxOfCharacteristics)):										#Recorrera el contenido de la caja, para obtener los vetices.
			currentLine = textOfBoxOfCharacteristics[i]											#Linea actual
			if(currentLine.find('\t') == -1):													#El vertice(no tiene \t)
				#print(currentLine)
				findItem = ("\t%s" % currentLine)
				for j in range(len(textOfBoxOfCharacteristics)):
					currentItemSecundaryItem = textOfBoxOfCharacteristics[j]
					if(currentItemSecundaryItem == findItem):
						name = currentItemSecundaryItem.strip()											#Arista con el mismo nombre del vertice actual, para extraer sus caracteristicas.
						vertexLL.add(name,None,None,None,None,None)
						#print("%s,%s,%s,%s,%s,%s" % (name,bandwidth,usersOnline,traffic,distance,meanType))
						break
		for k in range(len(textOfBoxOfCharacteristics)):						#Recorrera el contenido de la caja, para obtener las aristas.
			itemVertex = textOfBoxOfCharacteristics[k]
			if(itemVertex.find('\t') == -1):
				if(vertexLL.searchInLL(itemVertex,1) == True):
					for m in range(len(textOfBoxOfCharacteristics)):
						currentEdge = textOfBoxOfCharacteristics[m]	
						if(currentEdge == itemVertex):
							index = m + 1
							if(index < len(textOfBoxOfCharacteristics)):
								while(textOfBoxOfCharacteristics[index].count('\t') >= 1):
									if(textOfBoxOfCharacteristics[index].count('\t') == 1):
										name = textOfBoxOfCharacteristics[index].strip()
										distance = self.extractValueToString(textOfBoxOfCharacteristics[index+1]).strip()
										bandwidth = self.extractValueToString(textOfBoxOfCharacteristics[index+2]).strip()
										usersOnline = self.extractValueToString(textOfBoxOfCharacteristics[index+3]).strip()
										traffic = self.extractValueToString(textOfBoxOfCharacteristics[index+4])
										meanType = self.extractValueToString(textOfBoxOfCharacteristics[index+5])
										#print("%s,%s,%s,%s,%s,%s"%(name,distance,bandwidth,usersOnline,traffic,meanType))
										vertexLL.searchInLL(itemVertex).edges.add(name,bandwidth,usersOnline,traffic,distance,meanType)
									index +=1
		#vertexLL.first.next.edges._printToNormal()
		return vertexLL

	#Convierte los datos extraidos del texto que fueron almacenados en una LL, a un diccionario, para luego crear el mapa.
	def convertLLInDict(self,LLOfVertex):
		graph = Graph()
		LLOfEdges = LinkedList()
		for i in range(LLOfVertex.length()):											#Recorre los vertices de la lista enlazada.
			currentVertex = LLOfVertex.atPosition(i)									#Vertice actual.
			vertex = Vertex(currentVertex.name)
			LLOfEdges.add(currentVertex.name,vertex,None,None,None,None)					#Almacena los vertices 
			
		for j in range(LLOfVertex.length()):
			currentVertex = LLOfVertex.atPosition(j)
			vertex = LLOfEdges.searchInLL(currentVertex.name).distance
			for k in range(currentVertex.edges.length()):
				edge = currentVertex.edges.atPosition(k)					#Nodo arista
				objEdge = LLOfEdges.searchInLL(edge.name)					#Nodo arista(class vertex)
				vertex.addEdge(objEdge,edge.distance,edge.bandwidth,edge.usersOnline,edge.traffic,edge.meanType)
			graph.addVertex(vertex)

		return graph

	#Extrae el valor de una caracteristica(str). ej: Distancia:100 => 100
	def extractValueToString(self,string,toFind = ":"):
		indexFindChar = string.find(toFind)
		_len = len(string)
		newChar = string[indexFindChar+1 : _len]
		return newChar

	#Activa un texto en la pantalla, mandando como parametro el texto a mostrar.
	def enableLabel(self,state,text = ''):
		self.labelTextMessage.setVisible(state)
		self.labelTextMessage.setEnabled(state)
		self.labelTextMessage.setText(text)
		self.labelTextMessage.setStyleSheet('QLabel {color: red}')
		self.labelTextMessage.setFont(QFont("Times Font", 10))	
	
	#Centrado de la ventana.
	def centerWindow(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move(size.width()*1.5,size.height())

	#Abre la ventana que muetra el mapa.
	def openMapWindow(self):
		self.a = MapWindow()
		self.a.show()
	
	#Abre la ventana que muestra la tabla.
	def openTableWindows(self,content):
		self.b = TableWindow(content)
		self.b.show()

#Ventana que se crea para cargar la imagen del grafo.
class MapWindow(QDialog):
	def __init__(self, parent = None):
		QDialog.__init__(self, parent)
		self.setWindowTitle("Grafica del grafo")
		
		label = QLabel(self)
		pixmap = QPixmap('graph.png')
		pixmap.scaled(20, 20)
		label.setPixmap(pixmap)
		self.resize(pixmap.width(),pixmap.height())

class TableWindow(QWidget):
	def __init__(self,contentPaths):
		QWidget.__init__(self)
		self.contentPaths = contentPaths
		self.setWindowTitle("Tabla de rutas")
		self.setGeometry(0,0,750,400)										#Ancho,alto
		self.center()
		content = QTextEdit(self)
		content.setGeometry(0,0,750,400)
		content.setText(self.contentPaths)
		
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move(size.width()/2,size.height()/2)

		
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("IconImagen/Icono_Programa.png"))

	window = PWindow()
	window.setWindowTitle("Mapa de grafos")

	window.show()
	sys.exit(app.exec_())

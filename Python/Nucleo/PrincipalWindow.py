# -*- coding: utf-8 -*-
#from recursiveJson import *
from LinkedList import *
from BuildGraf import *
from QuickSort import *
from eventMouse import *
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
		self.setGeometry(0,0,450,650)					
		QMainWindow.setWindowFlags(self, core.Qt.FramelessWindowHint)
		self.boxsText()
		self.buttons()	
		self.objectGraph = None
		
		paint = """
		QMainWindow{
	  	background-color:#3B8A9B;
	  	color:black;
		background-image: url("Imagenes/barra.jpg");
	  	background-repeat:no-repeat;
		background-position:center top;
		}QPushButton{
			background-color:#00486e;
			color:white;
			font-size: 300%;
			border-style: none;
			border-radius: 7;
			padding: 5px;
			padding-left: 7px;
			padding-right: 30px;
			border-color: darkblue;
			border-width: 2px;
			font-family:Times Font;		
		}
		"""

		self.setStyleSheet(paint)
		self.centerWindow()

	#Define y establece las cajas de texto para la ruta origen y destino.
	def boxsText(self):
		self.boxOfCharacteristics = QTextEdit(self)	#(x,y,tamanoX,tamanoY)
		self.boxOfCharacteristics.setGeometry(10,60,430,380)
			
		self.boxOfOrigin = QLineEdit(self)
		self.boxOfOrigin.setPlaceholderText("Nodo origen")
		self.boxOfOrigin.setGeometry(10,450,210,40)

		self.boxOfDestination = QLineEdit(self)
		self.boxOfDestination.setPlaceholderText("Nodo Destino")
		self.boxOfDestination.setGeometry(231,450,210,40)

		self.labelTextMessage = QLabel(self)
		self.labelTextMessage.setEnabled(False)
		self.labelTextMessage.setGeometry(10,480,400,40)

		self.font = QFont()
		self.font.setBold(True)
		self.font.setUnderline(True)

		self.labelTitle = QLabel(self)
		self.labelTitle.setGeometry(0,10,460,30)
		self.labelTitle.setStyleSheet('color: white')
		self.labelTitle.setFont(self.font)
		self.labelTitle.setText("PACKET TRACER")
		self.labelTitle.setAlignment(core.Qt.AlignHCenter | core.Qt.AlignVCenter)


	#Creacion de los botones de la ventana.
	def buttons(self):
		
		self.btnFileUpload = hoverButton(self)
		self.btnFileUpload.setFont(QFont("Times Font", 10))
		self.btnFileUpload.setText("Cargar archivo")
		self.btnFileUpload.setGeometry(10,510,210,60)
		self.btnFileUpload.setCursor(Qt.PointingHandCursor)
		self.btnFileUpload.setAutoDefault(False)
		self.btnFileUpload.setToolTip("Cargar un archivo de texto.")
		self.btnFileUpload.clicked.connect(self.enableButtonUpload)

		self.btnCreateMap = hoverButton(self)
		self.btnCreateMap.setFont(QFont("Times Font", 10))
		self.btnCreateMap.setText("Crear mapa")
		self.btnCreateMap.setGeometry(231,510,210,60)
		self.btnCreateMap.setCursor(Qt.PointingHandCursor)
		self.btnCreateMap.setAutoDefault(False)
		self.btnCreateMap.setToolTip("Crear un mapa con el contenido actual.")
		self.btnCreateMap.clicked.connect(self.enableCreateMap)
		
		self.btnCreateTable = hoverButton(self)
		self.btnCreateTable.setFont(QFont("Times Font", 10))
		self.btnCreateTable.setText("Crear tabla")
		self.btnCreateTable.setGeometry(120,580,210,60)
		self.btnCreateTable.setCursor(Qt.PointingHandCursor)
		self.btnCreateTable.setAutoDefault(False)
		self.btnCreateTable.setToolTip("Crear tabla de rutas.")
		self.btnCreateTable.clicked.connect(self.enableButtonCreateTable)

		self.minimize = QToolButton(self)
		self.minimize.setGeometry(395,10,20,10)
		self.minimize.setStyleSheet('background-color:#00486e;border-style:none')
		self.minimize.setIcon(QIcon("Imagenes/minimizeButton.png"))
		self.minimize.clicked.connect(self.minimizeWindow)
		self.minimize.setToolTip("Minimizar")

		self.close = QToolButton(self)
		self.close.setIcon(QIcon('Imagenes/closeButton.png'))
		self.close.setGeometry(412,10,40,30)
		self.close.setStyleSheet('background-color:#00486e;border-style:none')
		self.close.clicked.connect(self.closeWindow)
		self.close.setToolTip("Cerrar")

		self.minimize.setMinimumHeight(30)
		self.close.setMinimumHeight(30)

	#Ordenamiento por cajas de los widgets.
	def layoutPWindow(self):
		
		self.hBoxCharacteristicsLayout = QHBoxLayout()
		self.hBoxCharacteristicsLayout.addWidget(self.boxOfCharacteristics)

		self.hBoxOriginAndDestinyLayout = QHBoxLayout()
		self.hBoxOriginAndDestinyLayout.addWidget(self.boxOfOrigin)
		self.hBoxOriginAndDestinyLayout.addWidget(self.boxOfDestination)
		
		self.hButtonsUploadAndCreateMapLayout = QHBoxLayout()
		self.hButtonsUploadAndCreateMapLayout.addWidget(self.btnFileUpload)
		self.hButtonsUploadAndCreateMapLayout.addWidget(self.btnCreateMap)
		self.hButtonsUploadAndCreateMapLayout.setGeometry(QRect(10,700,220,50))
		
		self.hPrincipalTitle = QHBoxLayout(self)
		self.hPrincipalTitle.addWidget(self.minimize)
		self.hPrincipalTitle.addWidget(self.close)
		self.hPrincipalTitle.insertStretch(0)
		self.hPrincipalTitle.setSpacing(0)
		self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
		self.maxNormal = False

		self.hPrincipaPositionTitle = QHBoxLayout(self)
		self.hPrincipaPositionTitle.addWidget(self.labelTitle)
		self.hPrincipaPositionTitle.addLayout(self.hPrincipalTitle)		

		self.vFinalLayout = QVBoxLayout()
		self.vFinalLayout.addLayout(self.hPrincipaPositionTitle)
		self.vFinalLayout.addWidget(self.labelTextMessage)
		self.vFinalLayout.addLayout(self.hButtonsUploadAndCreateMapLayout)

		self.orderingLayout = QWidget()
		self.orderingLayout.setLayout(self.vFinalLayout)
		self.setCentralWidget(self.orderingLayout)


#-----------------FUNCIONES GENERALES------------------
	#Funcion que se activa al presionar el boton de crear mapa.
	def enableCreateMap(self):
		G = nx.DiGraph()
		fig = plt.figure()
		self.enableLabel(False)
		LLOfVertex = self.extractValuesToTextFormat()		
		if(LLOfVertex != ""):
			self.objectGraph = self.convertLLInDict(LLOfVertex)
			saveWeightOfPaths = []

			#Recorre el diccionario creado del texto, extrayendo sus llaves,valores,peso para dibujar.
			if(self.objectGraph != None):											#Si hay un diccionario.
				g = self.objectGraph.vertices
				for k,v in g.items():
					for aris,w in v.items():
						G.add_node(str(k))
						G.add_edge(str(k), str(aris),weight=str(w))

				#Agrega 2 pesos en las aristas, ejm: A-B y de B-A
				pos = nx.circular_layout(G)
				labels = nx.get_edge_attributes(G,'weight')							#Devuelve el diccionario que contiene todo el grafo.
				for key,w in labels.items():
					concatenate = str(key[0] + str(key[1]))
					concatenate = concatenate.replace(" ", "")
					saveWeightOfPaths.append(concatenate)
					if(self.searchPathsSaved(key[0],key[1],saveWeightOfPaths) == True):
						weigth = self.objectGraph.searchEdgeWeight(key[1],key[0])	
						labels[key] = ("(%s)►\n◄(%s)"%(weigth,w))	

				#Establece y determina el dibujado utilizando 'nx'.
				nx.draw_circular(G,arrows=True,with_labels=True,node_color='skyblue',node_size=2500,edge_color='red',arrowsize=10,font_color='white',font_size=9)
				nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_family='sans-serif',font_size=7)
				
				#fig.set_facecolor("#00000F")
				fig.set_facecolor('white')
				plt.savefig('graph.png',facecolor=fig.get_facecolor() )				#Guarda la imagen dado una ruta.
				
				self.openMapWindow()													#Abre otra ventana para mostrar el mapa creado.
			else:
				self.enableLabel(True,"No hay un archivo cargado para dibujar el mapa.")
		else:
			self.enableLabel(True,"No hay contenido escrito.")
	#Carga el archivo de texto, y lo excribe en la caja de EditText
	def enableButtonUpload(self):
		filePath = QFileDialog.getOpenFileName(self, "Selecciona el archivo a cargar.")
		filePath = filePath[0]		
		if(filePath != ''):																#Si se ha elegido un archivo, caso contrario muestra un mensaje.
			tempList = self.extractContentToBoxOfCharacteristics(filePath)				#Guarda el contenido extraido del archivo cargado.
			self.content = "".join(tempList)											
			self.boxOfCharacteristics.setText(self.content)								#Traspasa el contenido cargado a la caja de texto.

	#Funcion que usa al presionar el boton crear tabla.
	def enableButtonCreateTable(self):
		LLOfVertex = self.extractValuesToTextFormat()
		if(LLOfVertex != ""):		
			self.objectGraph = self.convertLLInDict(LLOfVertex)
			
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
				destination = self.boxOfDestination.text()										#Extrae el texto de la caja destino.
				stateO,stateD = self.checkVertexExists(origin,destination,newJson)

				#------------Control del input del origen y dpyestino------------
				if(stateO == True and stateD == True):										#En caso que los valores de las cajas, existan en el diccionario.
					buildPaths.findPaths(origin,destination,newJson)						#Busca todas las rutas desde el punto origen, al destino.
					paths = buildPaths.getPaths()											#Devuelve y guarda las rutas encontradas.
					self.labelTextMessage.setVisible(False)
					
					title = ("%s\n%s%s%s\n%s\n" % ('='*107,'\t'*4,'T A B L A  D E  R U T A S\n','\t\t\t---La ruta mas optima, es la de mayor peso(confiabilidad)---','='*107))
					labelPath = ("\t\t\t\tRuta desde %s hasta %s\n"% (origin,destination))
					titleSubTable = ("%s" % ('\tPeso\t|\tRuta\n'))
					dates = ""
					
					#Este ciclo recorrera todos las rutas, para guardarlas en una LL, para asi mas adelante poder ordenar las rutas desde el menor peso, al mayor peso...
					#...por el cual el primer o primeros elementos de la lista en tabla, sera la ruta mas corta.
					for i in paths:																					#Ruta de vertices
						weight = self.searchWeight(i,self.objectGraph)
						LLOfPathsAndWeigth.add(i,weight,None,None,None,None)										#name:ruta,distance:peso
						arrWeight.append(weight)
					sort.execution(arrWeight)
					tempPath = []
					for j in arrWeight:
						state = True
						for k in range(LLOfPathsAndWeigth.length()):
							currentNode = LLOfPathsAndWeigth.atPosition(k)
							if(j == currentNode.distance and currentNode.name not in tempPath and state == True):															#En el atributo distance esta guardado el peso.
								tempPath.append(currentNode.name)
								temp = ("%s\n\t%s\t|\t%s\n" % ('-'*190,j,",".join(currentNode.name)))
								dates = dates + temp
								state = False
							
					content = title + labelPath + titleSubTable + dates															#Contiene todo el contenido a mostrar en la ventana de la tabla.
					self.openTableWindows(content)
				
				elif(stateO == True and stateD == False):
					self.enableLabel(True,'El valor destino no existe')
				
				elif(stateO == False and stateD == True):
					self.enableLabel(True,'El valor origen no existe')
				
				elif(stateO == False and stateD == False):
					self.enableLabel(True,'El valor origen y destino no existen')
			else:
				self.enableLabel(True,"No hay un archivo cargado para obtener la tabla.")
		else:
			self.enableLabel(True,"No hay contenido escrito.")

	#-----------------------------FUNCIONES LLAMADAS POR LAS GENERALES----------------------------------------------
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

	#Esta funcion es utilizada a la hora de dibujar los pesos entre las aristas, para poder mostrar ambos pesos, ejm: peso de A - B y peso de B - A => (5,4)
	def searchPathsSaved(self,path1,path2,arr):
		item = ("%s%s" % (str(path2),str(path1)))
		item = item.replace(" ", "")
		for i in arr:
			if(i == item): 
				return True
	
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
		if(textOfBoxOfCharacteristics !=""):
			textOfBoxOfCharacteristics = textOfBoxOfCharacteristics.split('\n')
			vertexLL = LinkedList()
			for i in range(len(textOfBoxOfCharacteristics)):										#Recorrera el contenido de la caja, para obtener los vetices.
				currentLine = textOfBoxOfCharacteristics[i]											#Linea actual
				if(currentLine.find('\t') == -1):													#El vertice(no tiene \t)
					findItem = ("\t%s" % currentLine)
					for j in range(len(textOfBoxOfCharacteristics)):
						currentItemSecundaryItem = textOfBoxOfCharacteristics[j]
						if(currentItemSecundaryItem == findItem):
							name = currentItemSecundaryItem.strip()											#Arista con el mismo nombre del vertice actual, para extraer sus caracteristicas.
							vertexLL.add(name,None,None,None,None,None)
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
											vertexLL.searchInLL(itemVertex).edges.add(name,bandwidth,usersOnline,traffic,distance,meanType)
										index +=1
			return vertexLL
		else:
			return ""
			self.enableLabel(True,"No hay contenido para extraer.")

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
		self.labelTextMessage.setStyleSheet('QLabel {color: darkred}')
		self.labelTextMessage.setFont(QFont("Times Font", 11))	
	
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

	#Funcion al boton minimizar ventana.
	def minimizeWindow(self):
		self.showMinimized()

	#Funcion al boton cerrar ventana.
	def closeWindow(self):
		sys.exit()
	

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


#Clase para generar la ventana de la tabla de rutas.
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

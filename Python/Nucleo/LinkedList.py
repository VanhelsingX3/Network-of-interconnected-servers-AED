class Node:
	def __init__(self,name,distance,bandwidth,usersOnline,traffic,meanType):
		self.name = name
		self.distance = distance
		self.bandwidth = bandwidth
		self.usersOnline = usersOnline
		self.traffic = traffic
		self.meanType = meanType
		self.edges = LinkedList()
		self.next = None

class LinkedList:
	def __init__(self):
		self.first = None
		
	def add(self,name,distance,bandwidth,usersOnline,traffic,meanType):
		if(not self.first):
			self.first = Node(name,distance,bandwidth,usersOnline,traffic,meanType)
		
		else:
			current = self.first
			while(current.next):
				current = current.next
			current.next = Node(name,distance,bandwidth,usersOnline,traffic,meanType)
	
	#Buscar en la lista.
	def searchInLL(self,name,state = 0):			#Busqueda de un elemento, state =0 para devolver el nodo, state = 1 para regresar un boolean
		current = self.first
		if(state == 0):
			if(self.first.name == name):
				return self.first
			else:
				while (current.next):
					current = current.next
					if(current != None):
						if (current.name == name):
							return current
		
		elif(state == 1):
			if(current.name == name):
				return True
			else:
				while (current.next):
					current = current.next
					if (current.name == name):
						return True
				return False

	#Obtener el tamano de la lista.
	def length(self):
		current = self.first
		if(current !=None):
			size = 1
			while(current.next):
				current = current.next
				size += 1
			return size
		else:
			return 0

	#Obtener un item dado un indice.
	def atPosition(self,index):
		tam = self.length()
		current = self.first
		if(index >= tam):
			print("busqueda fuera de rango")
			return -1
		else:
			if(index == 0):
				return current
			else:
				count = 0
				while(current.next):
					current = current.next
					count +=1
					if(count == index):
						return current
						
	#Imprime los elementos de la lista	
	def _printToNormal(self,state = None):						
		current = self.first
		if(current != None):
			while (current.next):
				if(state==1):
					print(current)
				else:
					print (current.name)
				current = current.next
			if(state == 1):
				print(current)
			else:
				print (current.name)
		else:
			return None

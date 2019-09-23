#Algoritmo de ordenamiento.
class QuickSort:
	def __init__(self):
		pass

	def execution (self,array=[]):									#Recibe el arreglo a ordenar.
		return self.quickSort(array,0,len(array)-1)				#Hace llamado a la siguiente funcion.

	def quickSort(self,array,low,high):
		if low < high:											#Ordenamiento por seleccion de pivote.
			pivot = self.partition(array,low,high)
			self.quickSort(array,low,pivot-1)						#Particion 1(izquierda pivote)
			self.quickSort(array,pivot+1,high)					#Particion 2(derecha pivote)
	
	def partition(self,array,low,high):
		i = (low-1)
		pivot = array[high]
		for j in range(low,high):
			if array[j] <= pivot:
				i = i+1
				array[i],array[j] = array[j],array[i]
		array[i+1],array[high] = array[high],array[i+1]
		return (i+1)
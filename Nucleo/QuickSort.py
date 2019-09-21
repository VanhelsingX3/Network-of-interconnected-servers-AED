#Algoritmo de ordenamiento.
class QuickSort:
	def __init__(self):
		pass

	def sort (self,array=[]):									#Recibe el arreglo a ordenar.
		return self.quickSort(array,0,len(array)-1)				#Hace llamado a la siguiente funcion.

	def quickSort(self,arr,low,high):
		if low < high:											#Ordenamiento por seleccion de pivote.
			pivot = self.partition(arr,low,high)
			self.quickSort(arr,low,pivot-1)						#Particion 1(izquierda pivote)
			self.quickSort(arr,pivot+1,high)					#Particion 2(derecha pivote)
	

	def partition(self,arr,low,high):
		i = (low-1)
		pivot = arr[high]
		for j in range(low,high):
			if arr[j] <= pivot:
				i = i+1
				arr[i],arr[j] = arr[j],arr[i]
		arr[i+1],arr[high] = arr[high],arr[i+1]
		return (i+1)
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
                
"""
graph = {
        'A': ['B','E'],
        'B': ['A','C','D'],
        'C': ['B'],
        'D': ['B','G','E'],
        'E': ['A','D','F'],
        'F': ['E','G'],
        'G': ['D','F'],
        }

building = BuildPaths()
building.findPaths('A','C',graph)
print(building.paths)
"""
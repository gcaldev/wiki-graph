import random


class Grafo:
    """Representa un grafo dirigido o no dirigido"""
    
    def __init__(self, es_dirigido = False):
        self.vertices = {}
        self.es_dirigido = es_dirigido
        self.cantidad = 0
    
    def __len__(self):
        """Devuelve la cantidad de vertices que tiene el grafo"""
        return self.cantidad

    def agregar_vertice(self,v):
        """Agrega un nuevo vertice al grafo, devuelve true en caso de que se haya podido agregar, false en caso contrario"""
        if not v in self.vertices.keys():
            self.vertices[v] = dict()
            self.cantidad += 1
            return True
        return False

    def borrar_vertice(self,v):
        """Elimina el vertice del grafo, devuelve False en caso de que no se encuentre"""
        if not v in self.vertices.keys():
            return False
        self.vertices.remove(v)
        for vertice in self.vertices.keys():
            if v in self.vertices[vertice]:
                self.vertices[vertice].remove(v)
        self.cantidad -= 1
        return True

    def agregar_arista(self, v, w, peso = 1):
        """Agrega una arista de v a w en caso de ser dirigido, agrega en ambos sentidos en caso de ser no dirigido"""
        if not v in self.vertices.keys() or not v in self.vertices.keys():
            raise ValueError
        self.vertices[v][w] = peso
        if not self.es_dirigido:
            self.vertices[w][v] = peso



    def borrar_arista(self, v, w):
        """Elimina una arista de """
        if not v in self.vertices.keys() or not v in self.vertices.keys():
            raise ValueError
        self.vertices[v].remove(w)
        if not self.es_dirigido:
            self.vertices[w].remove(v)
    
    def estan_unidos(self, v, w):
        """Devuelve True si el vertice v tiene una arista a w, si es no dirigido verifica que ambas relaciones se cumplan"""
        if self.es_dirigido:
            return w in self.vertices[v]
        return w in self.vertices[v] and v in self.vertices[w]

    def peso_arista(self, v, w):
        """Devuelve el peso de la arista entre v y w"""
        if not w in self.vertices[v].keys():
            return None
        return self.vertices[v][w]

    def obtener_vertices(self):
        """Devuelve un arreglo con todos los vertices del grafo"""
        arr = []
        for vertice in self.vertices.keys():
            arr.append(vertice)
        return arr

    def vertice_aleatorio(self):
        """Devuelve un vertice aleatorio del grafo"""
        if not self.vertices:
            return None
        return list(self.vertices.keys())[0]
        
    def adyacentes(self, v):
        """Devuelve los adyacentes de un vertice"""
        arr = []
        if not self.vertice_pertenece(v):
            return arr
        if not self.vertices[v]:
            return arr
        for vertice in self.vertices[v].keys():
            arr.append(vertice)
        return arr

    def vertice_pertenece(self,v):
        """Devuelve true si el vertice pertenece al grafo"""
        return v in self.vertices.keys()
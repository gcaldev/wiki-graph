from os import terminal_size
from cola import Cola
from grafo_tda import Grafo
from pila import Pila


LINKS_A_RECORRER = 20
PAGINA_CORTE = "Filosofía"
CANTIDAD_ITER = 50



def crear_grafo_tsv(archivo):
    """Crea un grafo a partir de un archivo TSV en el que el primer elemento es vertice y los siguientes son sus adyacentes"""
    graph = Grafo(es_dirigido = True)
    with open(archivo, encoding = "utf-8") as f_pointer:
        while True:
            line = f_pointer.readline().rstrip("\n")
            if not line:
                break
            elements = line.split("\t")
            graph.agregar_vertice(elements[0])
            for i in range(1,len(elements)):
                if not graph.vertice_pertenece(elements[i]):
                    graph.agregar_vertice(elements[i])
                graph.agregar_arista(elements[0],elements[i])
    return graph


def caminos_min_sin_peso(grafo, origen):
    """Devuelve todos los caminos minimos de un grafo no dirigido"""
    padres = {}
    ord = {}
    visitados = set()
    cola = Cola()
    cola.encolar(origen)
    visitados.add(origen)
    ord[origen] = 0
    padres[origen] = None

    while not cola.esta_vacia():
        v = cola.desencolar()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                cola.encolar(w)
                padres[w] = v
                ord[w] = ord[v] + 1
                visitados.add(w)
    
    return padres, ord


def camino_mas_corto(grafo, origen, destino):
    """Devuelve el camino mas corto entre la pagina de origen y la de destino"""
    caminos, costos = caminos_min_sin_peso(grafo, origen)
    recorrido = []
    actual = destino
    if not destino in caminos:
        return None
    return reconstruir_camino(caminos, origen,destino),costos[destino]


def todos_en_rango(grafo, pagina, n):
    """Devuelve la cantidad de paginas que se encuentran a distancia n de la pagina"""
    contador = 0
    _, distancias = caminos_min_sin_peso(grafo, pagina)
    for v in distancias:
        if distancias[v] == n:
            contador += 1
    return contador


def reconstruir_camino(recorrido,origen,destino):
    """Reconstruye el camino de un recorrido a partir de su diccionario de padres"""
    if not destino in recorrido:
        return None
    actual = destino
    res = []
    while actual != None:
        res.append(actual)
        actual = recorrido[actual]
    return res[::-1]


def _navegar_primer_link(grafo, padre, pagina, n, contador, visitados, resultado):
    if n == contador or pagina == PAGINA_CORTE:
        return resultado
    resultado.append(pagina)
    visitados[pagina] = padre
    adyacentes = grafo.adyacentes(pagina)
    if not adyacentes:
        return resultado
    return _navegar_primer_link(grafo, pagina, adyacentes[0], n, contador + 1, visitados, resultado)


def navegar_primer_link(grafo, pagina):
    """Devuelve un recorrido yendo por el primer link hasta que: se encuentre con la palabra indicada, no haya mas paginas por recorrer o haya llegado a n paginas"""
    n = LINKS_A_RECORRER
    contador = 0
    visitados = {}
    visitados[pagina] = None
    adyacentes = grafo.adyacentes(pagina)
    if not adyacentes:
        return [pagina]
    return _navegar_primer_link(grafo, pagina, adyacentes[0], n, contador, visitados, [pagina])


def dfs_encontrar_ciclo(grafo, v, visitados, padres, n, contador, origen):
    for w in grafo.adyacentes(v):
        if v == w:
            continue
        if w in visitados:
            if w == origen: 
                if contador == n:  #Encontramos un ciclo de largo n ya que llegamos desde otro vertice al vertice de origen
                    return v

    if contador == n:
        # Si entra en esta condicion hacemos poda y comenzamos a borrar el recorrido hecho por la rama actual
        padres.pop(v)
        visitados.remove(v)
        return None

    for w in grafo.adyacentes(v):
        if not w in visitados:
            visitados.add(w)
            padres[w] = v
            ultimo_vertice = dfs_encontrar_ciclo(grafo, w, visitados, padres, n, contador + 1, origen)
            if ultimo_vertice:
                return ultimo_vertice
    padres.pop(v)
    visitados.remove(v)


def ciclo_de_n(grafo, origen, n):
    """Devuelve un ciclo del largo indicado"""
    if not n:
        return None
    if n == 1:
        if origen in grafo.adyacentes(origen):
            return [origen]
        return None
    visitados = set()
    padres = {}
    contador = 1
    padres[origen] = None
    visitados.add(origen)
    ultimo_vertice = dfs_encontrar_ciclo(grafo, origen, visitados, padres, n, contador, origen)
    return reconstruir_camino(padres, origen, ultimo_vertice)


def crear_grafo_paginas(grafo, paginas):
    """Crea un nuevo grafo a partir del grafo original, unicamente con las paginas indicadas"""
    g = Grafo(es_dirigido = True)
    for v in grafo.obtener_vertices():
        if not v in paginas:
            continue
        g.agregar_vertice(v)
        for w in grafo.adyacentes(v):
            if not w in paginas:
                continue
            if not g.vertice_pertenece(w):
                g.agregar_vertice(w)
            g.agregar_arista(v,w)
    return g

def dfs(grafo, visitados, visitados_rama, resultado, v):
    visitados.add(v)
    visitados_rama.add(v)
    for w in grafo.adyacentes(v):
        if w in visitados_rama:
            return None
        if not w in visitados:
            if not dfs(grafo, visitados, visitados_rama, resultado, w):
                return None
    resultado.append(v)
    visitados_rama.remove(v)
    return True


def orden_2am_dfs(grafo, paginas):
    """Devuelve un orden de lectura posible entre las paginas indicadas"""
    visitados = set()
    resultado = []
    g = crear_grafo_paginas(grafo,paginas)
    for v in g.obtener_vertices():
        if not v in visitados:
            if not dfs(g, visitados, set(),resultado, v):
                return None
    return resultado



def hallar_cfcs(grafo, visitados, apilados, pila, ord, orden_actual, v, mb, actual_cfc, total):
    visitados.add(v)
    ord[v] = orden_actual + 1
    mb[v] = orden_actual + 1
    orden_actual += 1
    pila.apilar(v)
    apilados.add(v)
    for w in grafo.adyacentes(v):
        if not w in visitados:
            orden_actual = hallar_cfcs(grafo, visitados, apilados, pila, ord, orden_actual, w, mb, actual_cfc, total)

        if w in apilados:
            mb[v] = min(mb[v],mb[w])

    if ord[v] == mb[v] and not pila.esta_vacia(): # Si son iguales significa q hay cfc y desapilamos hasta ver el vertice v
        actual_cfc = set()
        while True:
            w = pila.desapilar()
            apilados.remove(w)
            actual_cfc.add(w)
            if w == v:
                break
        total.append(actual_cfc)
    return orden_actual

def conectividad(grafo,pagina):
    """Devuelve el conjunto de paginas fuertemente conexas con la pagina recibida"""
    visitados = set()
    apilados = set()
    total = []
    actual = set()
    pila = Pila()
    ord = {}
    orden_actual = 0
    mb = {}
    hallar_cfcs(grafo, visitados, apilados, pila, ord, orden_actual, pagina, mb, actual, total)
    # Nos fijamos en que cfc forma parte la pagina y la devolvemos
    for cfc in total:
        if pagina in cfc:
            return cfc


def obtener_diametro(grafo):
    """Devuelve el recorrido del mayor camino minimo del grafo recibido"""
    max_min_dist = 0
    max_recorrido = None
    destino = None
    origen = None
    diametro = None
    for v in grafo.obtener_vertices():
        padres, distancias = caminos_min_sin_peso(grafo, v)
        for w in distancias:
            if distancias[w] > max_min_dist:
                max_min_dist = distancias[w]
                destino = w
                origen = v
                recorrido = padres
    diametro = reconstruir_camino(recorrido, origen, destino)
    return diametro,max_min_dist


def max_freq(vertice, labels, ady_entrada):
    """Devuelve la etiqueta que aparece con mayor frequencia entre los adyacentes"""
    freqs_adyacentes = {}
    for w in ady_entrada[vertice]:
        if not labels[w] in freqs_adyacentes:
            freqs_adyacentes[labels[w]] = 1
        else:
            freqs_adyacentes[labels[w]] += 1
    actual_freq = 0
    max_label = None
    for label, freq in freqs_adyacentes.items(): # Buscamos la label que mas aparecio
        if freq >= actual_freq:
            actual_freq = freq
            max_label = label
    return max_label


def _deteccion_comunidades(grafo):
    vertices = grafo.obtener_vertices()
    labels = {}
    ady_entrada = {}
    for v in vertices:
        labels[v] = v
        ady_entrada[v] = set()
    for v in vertices:
        for w in grafo.adyacentes(v):
            ady_entrada[w].add(v) # Agregamos los adyacentes de entrada de cada vertice
    for i in range(CANTIDAD_ITER):
        for v in vertices:
            label = max_freq(v, labels, ady_entrada)
            if label:
                labels[v] = label
    return labels


def deteccion_comunidades(grafo,pagina):
    """Devuelve un conjunto con las paginas que pertenecen a la comunidad de la pagina recibida"""
    comunidades = _deteccion_comunidades(grafo)
    resultado = set()
    if not pagina in comunidades:
        return None
    for pag_actual,comunidad in comunidades.items():
        if comunidad == pagina or comunidad == comunidades[pagina]:
            resultado.add(pag_actual)
    return resultado

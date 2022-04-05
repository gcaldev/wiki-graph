#!/usr/bin/python3
from grafo_tda import Grafo
from cola import Cola
from pila import Pila
from funciones_grafos import *
import sys
import random
CANTIDAD_ITER = 5
COMANDOS = ["camino", "conectados", "lectura", "diametro", "rango", "comunidad", "navegacion", "ciclo"]
SEPARADOR_1 = " -> "
SEPARADOR_2 = ", "

def formatear_recorrido(resultado, separador):
    """Devuelve una cadena compuesta por los elementos recibidos con el formato deseado"""
    if not resultado:
        return None
    paginas = resultado
    cadena = ""
    for pagina in paginas:
        cadena += pagina + separador
    return cadena[:-len(separador)]


def main():
    temp_cfc = None # Guardamos la cfc con el formato adecuado
    temp_cfc_set = None # Guardaremos la cfc encontrada en la conectividad anterior
    if len(sys.argv) < 2:
        return
    diametro_de_grafo = None # Guardamos el diametro del grafo y su costo
    grafo = crear_grafo_tsv(sys.argv[1])
    sys.setrecursionlimit(100000)
    for line in sys.stdin:
        comando = line.split()[0]
        parametros = line[len(comando) + 1:].rstrip("\n").split(",") # Obtenemos los parametros descartando el comando
        if comando == "diametro":
            if not diametro_de_grafo:
                recorrido, costo = obtener_diametro(grafo)
                path_formateado = formatear_recorrido(recorrido, SEPARADOR_1)
                diametro_de_grafo = path_formateado, costo # Guardamos el diametro para que la proxima vez que lo soliciten sea mostrado en tiempo constante
            else:
                path_formateado, costo = diametro_de_grafo
            print(path_formateado)
            print(f"Costo: {costo}")
        if comando == "listar_operaciones":
            for operacion in COMANDOS:
                print(operacion)
        if comando == "lectura":
            resultado = orden_2am_dfs(grafo, parametros)
            if not resultado:
                print("No existe forma de leer las paginas en orden")
            else:
                print(formatear_recorrido(resultado, SEPARADOR_2))
        if comando == "conectados":
            if not temp_cfc_set or not parametros[0] in temp_cfc_set:
                temp_cfc_set = conectividad(grafo, parametros[0]) # Guardamos la cfc en un set para que la consulta de si se encuentra en esta sea O(1)
                temp_cfc = formatear_recorrido(temp_cfc_set, SEPARADOR_2)
            print(temp_cfc)
        if comando == "comunidad":
            paginas = deteccion_comunidades(grafo, parametros[0])
            print(formatear_recorrido(paginas, SEPARADOR_2))
        if comando == "navegacion" or comando == "navegación":
            resultado = navegar_primer_link(grafo, parametros[0])
            print(formatear_recorrido(resultado, SEPARADOR_1))
        if comando == "camino":
            resultado = camino_mas_corto(grafo, parametros[0], parametros[1])
            if resultado:
                recorrido, costo = resultado
                print(formatear_recorrido(recorrido, SEPARADOR_1))
                print(f"Costo: {costo}")
            else:
                print("No se encontro recorrido")
        if comando == "rango":
            print(todos_en_rango(grafo, parametros[0], int(parametros[1])))
        if comando == "ciclo":
            recorrido = ciclo_de_n(grafo, parametros[0], int(parametros[1]))
            if recorrido:
                cadena = formatear_recorrido(recorrido, SEPARADOR_1)
                cadena += SEPARADOR_1 + recorrido[0]
                print(cadena)
            else:
                print("No se encontro recorrido")

main()
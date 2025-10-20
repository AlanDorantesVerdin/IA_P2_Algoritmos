"""
Alan Dorantes Verdin

Algoritmo 1: Búsqueda en Anchura 

Descripción:
La Búsqueda en Anchura es un algoritmo de recorrido de grafos. Comienza en un nodo
raíz (o un nodo de inicio arbitrario) y explora todos los nodos vecinos a la
profundidad actual antes de moverse a los nodos del siguiente nivel de profundidad.

Características Principales:
1.  Usa una cola (Queue) para gestionar los nodos pendientes de visitar.
    Esto sigue una política FIFO (First-In, First-Out).
2.  Es un algoritmo "completo": si existe una solución (un camino al nodo objetivo),
    BFS la encontrará.
3.  Es "óptimo" si los costos de los caminos son uniformes (por ejemplo, cada
    arista vale 1). Encontrará el camino más corto en términos del número
    de aristas.
4.  Complejidad Temporal: O(V + E), donde V es el número de vértices (nodos)
    y E es el número de aristas (conexiones).
5.  Complejidad Espacial: O(V), ya que en el peor de los casos, la cola
    podría almacenar todos los vértices.

"""

from collections import deque

def busqueda_en_anchura(grafo, nodo_inicial, nodo_objetivo):
    """
    Implementación de la Búsqueda en Anchura (BFS).

    Argumentos:
    - grafo (dict): Una representación del grafo usando una lista de adyacencia.
                    Es un diccionario donde cada clave es un nodo y su valor
                    es una lista de nodos vecinos.
    - nodo_inicial (str/int): El nodo desde el cual comenzará la búsqueda.
    - nodo_objetivo (str/int): El nodo que queremos encontrar.

    Retorna:
    - list: El camino desde el nodo inicial al nodo objetivo, o None si no existe.
    """
    
    print(f"Iniciando Búsqueda en Anchura (BFS) desde el nodo: {nodo_inicial}")
    print(f"Buscando el nodo objetivo: {nodo_objetivo}\n")

    # Conjunto para llevar un registro de los nodos visitados
    visitados = set()

    # Cola que almacena tuplas: (nodo_actual, camino_hasta_ese_nodo)
    cola = deque([(nodo_inicial, [nodo_inicial])])

    # Marcamos el nodo inicial como visitado
    visitados.add(nodo_inicial)

    # Bucle principal
    while cola:
        
        # Sacamos el primer elemento de la cola
        nodo_actual, camino = cola.popleft()
        print(f"Visitando nodo: {nodo_actual} | Camino actual: {' -> '.join(camino)}")

        # Comprobamos si hemos llegado al nodo objetivo
        if nodo_actual == nodo_objetivo:
            print(f"\n¡Nodo objetivo '{nodo_objetivo}' encontrado!")
            print(f"Camino encontrado: {' -> '.join(camino)}")
            print(f"Longitud del camino: {len(camino) - 1} aristas")
            return camino

        # Exploramos los vecinos del nodo actual
        for vecino in grafo.get(nodo_actual, []):
            
            # Si el vecino no ha sido visitado...
            if vecino not in visitados:
                
                # Lo marcamos como visitado
                visitados.add(vecino)
                
                # Creamos un nuevo camino que incluye al vecino
                nuevo_camino = camino + [vecino]
                
                # Lo añadimos a la cola
                cola.append((vecino, nuevo_camino))
                print(f"  -> Encolando vecino: {vecino}")

    print(f"\nNo se encontró un camino al nodo objetivo '{nodo_objetivo}'.")
    return None

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    
    # Definimos un grafo de ejemplo usando un diccionario (lista de adyacencia)
    # A --- B --- E
    # |     |   / |
    # |     |  /  |
    # C --- D     F
    
    mi_grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'D'],
        'D': ['B', 'C', 'E'],
        'E': ['B', 'D', 'F'],
        'F': ['E']
    }

    # Llamamos a la función comenzando desde el nodo 'A' y buscando el nodo 'F'
    camino_encontrado = busqueda_en_anchura(mi_grafo, 'A', 'F')
    
    if camino_encontrado:
        print(f"\nResumen: El camino más corto de A a F es: {camino_encontrado}")
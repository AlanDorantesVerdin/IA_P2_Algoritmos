# Algoritmo 01. Búsqueda en Anchura
# Alan Dorantes Verdin

from collections import deque # Usamos deque para una cola eficiente

def busqueda_anchura(grafo, inicio, objetivo):
    """
    Encuentra el camino más corto (en nodos) de 'inicio' a 'objetivo' usando BFS.
    """
    # 1. Cola para nodos por visitar
    cola = deque([inicio])
    
    # 2. Conjunto de nodos ya visitados (para evitar ciclos)
    visitados = {inicio}
    
    # 3. Diccionario para reconstruir el camino
    # guarda: {nodo: nodo_padre}
    padres = {inicio: None}

    print(f"Iniciando BFS desde {inicio}...")

    while cola:
        # 4. Sacar el primer nodo de la cola
        nodo_actual = cola.popleft()
        print(f"Visitando: {nodo_actual}")

        # 5. Objetivo encontrado
        if nodo_actual == objetivo:
            print(f"¡Objetivo {objetivo} encontrado!")
            
            # Reconstruir camino
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino[::-1] # Devolver el camino invertido (inicio -> fin)

        # 6. Explorar vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)      # Marcar como visitado
                padres[vecino] = nodo_actual # Guardar el padre
                cola.append(vecino)        # Añadir a la cola

    print(f"Objetivo {objetivo} no alcanzable.")
    return None

# Ejemplo de grafo no ponderado representado como un diccionario
grafo_no_ponderado = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
    'G': [] # Un nodo aislado
}

# Ejemplo de uso
print("\n--- 1. Búsqueda en Anchura (BFS) ---")
camino_bfs = busqueda_anchura(grafo_no_ponderado, 'A', 'F')
print(f"Camino encontrado: {camino_bfs}\n")
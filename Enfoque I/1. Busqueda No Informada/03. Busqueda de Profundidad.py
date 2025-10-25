# Algoritmo 03. Búsqueda en Profundidad
# Alan Dorantes Verdin

def busqueda_profundidad(grafo, inicio, objetivo):
    """
    Encuentra UN camino (no necesariamente el más corto) usando DFS.
    Esta es una versión iterativa (usando pila).
    """
    # 1. Pila para nodos por visitar
    pila = [inicio]
    
    # 2. Conjunto de nodos ya visitados
    visitados = {inicio}
    
    # 3. Diccionario para reconstruir el camino
    padres = {inicio: None}
    
    print(f"Iniciando DFS desde {inicio}...")

    while pila:
        # 4. Sacar el último nodo de la pila
        nodo_actual = pila.pop()
        print(f"Visitando: {nodo_actual}")

        # 5. Objetivo encontrado
        if nodo_actual == objetivo:
            print(f"¡Objetivo {objetivo} encontrado!")
            # Reconstruir camino
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino[::-1]

        # 6. Explorar vecinos (en orden inverso para explorar alfabéticamente)
        # (Esto es opcional, pero hace que la traza sea más predecible)
        for vecino in sorted(grafo.get(nodo_actual, []), reverse=True):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = nodo_actual
                pila.append(vecino) # Añadir a la pila

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
print("\n--- 3. Búsqueda en Profundidad (DFS) ---")
camino_dfs = busqueda_profundidad(grafo_no_ponderado, 'A', 'F')
print(f"Camino encontrado: {camino_dfs}\n")
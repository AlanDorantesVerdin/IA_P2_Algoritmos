# Algoritmo 07. Búsqueda en Grafos
# Alan Dorantes Verdin

from collections import deque # Usamos deque para una cola eficiente

def busqueda_en_grafos_bfs(grafo, inicio, objetivo):
    """
    Implementación de "Búsqueda en Grafos" usando la estrategia BFS.
    """
    
    # 1. Cola para nodos por visitar
    cola = deque([inicio])
    
    # 2. El componente CLAVE de "Búsqueda en Grafos":
    # Un conjunto (memoria) de nodos que ya hemos visitado.
    # Esto evita que volvamos a procesar un nodo y caigamos en ciclos (ej. A->B->A->B...)
    visitados = {inicio}
    
    # 3. Diccionario para reconstruir el camino
    # guarda: {nodo: nodo_padre}
    padres = {inicio: None}

    print(f"Iniciando Búsqueda en Grafos (BFS) desde {inicio}...")

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
            
            # 7. LA VERIFICACIÓN CLAVE:
            # Si el vecino NO está en nuestra 'memoria' de visitados...
            if vecino not in visitados:
                # ...lo añadimos a la memoria...
                visitados.add(vecino)
                # ...guardamos su padre...
                padres[vecino] = nodo_actual
                # ...y lo añadimos a la cola para explorarlo después.
                cola.append(vecino)
            
            # Si 'vecino' YA estaba en 'visitados', simplemente lo ignoramos.

    print(f"Objetivo {objetivo} no alcanzable.")
    return None

# Ejemplo de un grafo no ponderado
grafo_no_ponderado = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
    'G': []
}

# Ejemplo de uso
print("\n--- 7. Búsqueda en Grafos (Ejemplo con BFS) ---")
camino_bfs = busqueda_en_grafos_bfs(grafo_no_ponderado, 'A', 'F')
print(f"Camino encontrado: {camino_bfs}\n")
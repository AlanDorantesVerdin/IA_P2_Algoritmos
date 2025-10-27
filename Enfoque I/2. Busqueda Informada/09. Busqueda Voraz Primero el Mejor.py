# Algoritmo 09. Búsqueda Voraz Primero el Mejor
# Alan Dorantes Verdin

import heapq

def busqueda_voraz(grafo, inicio, objetivo, h):
    """
    Encuentra un camino usando Greedy Best-First. No garantiza el camino óptimo.
    """
    # 1. Cola de prioridad (min-heap)
    # Almacena tuplas: (h(n), nodo_actual, nodo_padre)
    # Se ordena por h(n)
    cola_prioridad = [(h(inicio), inicio, None)]
    
    # 2. Visitados
    visitados = set()
    
    # 3. Padres
    padres = {inicio: None}

    print(f"Iniciando Búsqueda Voraz desde {inicio}...")

    while cola_prioridad:
        
        # 4. Sacar el nodo con MENOR heurística h(n)
        (heuristica, nodo_actual, padre) = heapq.heappop(cola_prioridad)

        if nodo_actual in visitados:
            continue
        
        print(f"Visitando: {nodo_actual} (h(n)={heuristica})")
        visitados.add(nodo_actual)
        padres[nodo_actual] = padre

        # 5. Objetivo encontrado
        if nodo_actual == objetivo:
            print(f"¡Objetivo {objetivo} encontrado!")
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino[::-1]

        # 6. Explorar vecinos
        # (Usamos el grafo ponderado, aunque la búsqueda ignora el costo de la arista)
        for vecino, costo_arista in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                # La prioridad es solo la heurística del vecino
                prioridad = h(vecino)
                heapq.heappush(cola_prioridad, (prioridad, vecino, nodo_actual))

    print(f"Objetivo {objetivo} no alcanzable.")
    return None

# Ejemplo de un grafo ponderado (aunque la búsqueda voraz no usa los costos)
grafo_ponderado = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 5)],
    'C': [('A', 2), ('F', 10)],
    'D': [('B', 5), ('E', 3)],
    'E': [('D', 3), ('F', 4)],
    'F': [('C', 10), ('E', 4)]
}

# Función heurística: estima la distancia desde cada nodo al objetivo F
def h(nodo):
    """
    Heurística que estima la distancia de cada nodo al objetivo F.
    Valores más bajos indican mayor cercanía al objetivo.
    """
    heuristicas = {
        'A': 7,  
        'B': 6,
        'C': 5,
        'D': 4,
        'E': 2,
        'F': 0
    }
    return heuristicas.get(nodo, float('inf'))

# Ejemplo de uso
print("\n--- 9. Búsqueda Voraz Primero el Mejor ---")
# Usamos el grafo ponderado (aunque ignora costos) y la heurística
camino_voraz = busqueda_voraz(grafo_ponderado, 'A', 'F', h)
print(f"Camino encontrado: {camino_voraz}\n")
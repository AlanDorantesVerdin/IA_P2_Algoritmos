# Algoritmo 02. Búsqueda de Anchura de Costo Uniforme
# Alan Dorantes Verdin

import heapq # Usamos heapq para la cola de prioridad

def busqueda_costo_uniforme(grafo, inicio, objetivo):
    """
    Encuentra el camino de menor costo de 'inicio' a 'objetivo' usando UCS.
    """
    # 1. Cola de prioridad (min-heap)
    # Almacena tuplas: (costo_acumulado, nodo_actual, nodo_padre)
    cola_prioridad = [(0, inicio, None)] # Costo inicial 0
    
    # 2. Conjunto de nodos ya visitados (para evitar ciclos)
    visitados = set()
    
    # 3. Diccionario para reconstruir el camino
    # guarda: {nodo: (nodo_padre, costo_para_llegar_a_nodo)}
    padres = {inicio: (None, 0)}

    print(f"Iniciando UCS desde {inicio}...")

    while cola_prioridad:
        
        # 4. Sacar el nodo con MENOR costo acumulado
        (costo_actual, nodo_actual, padre) = heapq.heappop(cola_prioridad)

        if nodo_actual in visitados:
            continue # Ya encontramos un camino más barato a este nodo

        print(f"Visitando: {nodo_actual} (Costo: {costo_actual})")
        
        # 5. Marcar como visitado y guardar su padre
        visitados.add(nodo_actual)
        padres[nodo_actual] = (padre, costo_actual)

        # 6. Objetivo encontrado
        if nodo_actual == objetivo:
            print(f"¡Objetivo {objetivo} encontrado con costo {costo_actual}!")
            
            # Reconstruir camino
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                # (ignorar el costo aquí, solo necesitamos el padre)
                nodo_actual = padres[nodo_actual][0] 
            return (camino[::-1], costo_actual)

        # 7. Explorar vecinos
        for vecino, costo_arista in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                nuevo_costo = costo_actual + costo_arista
                # Añadir a la cola de prioridad
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino, nodo_actual))

    print(f"Objetivo {objetivo} no alcanzable.")
    return None

# Ejemplo de grafo ponderado 
grafo_ponderado = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 5)],
    'C': [('A', 2), ('F', 10)],
    'D': [('B', 5), ('E', 3)],
    'E': [('D', 3), ('F', 4)],
    'F': [('C', 10), ('E', 4)]
}

# Ejemplo de uso
print("\n--- 2. Búsqueda de Costo Uniforme (UCS) ---")
camino_ucs = busqueda_costo_uniforme(grafo_ponderado, 'A', 'F')
print(f"Camino encontrado: {camino_ucs}\n")
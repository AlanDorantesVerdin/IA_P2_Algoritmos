# Algoritmo 06. Búsqueda Bidireccional
# Alan Dorantes Verdin

from collections import deque # Usamos deque para una cola eficiente

def reconstruir_camino(nodo_encuentro, visitados_inicio, visitados_objetivo):
    """
    Combina los caminos de ambas búsquedas a partir del nodo de encuentro.
    """
    
    # 1. Camino desde INICIO -> NODO_ENCUENTRO
    camino_inicio = []
    curr = nodo_encuentro
    while curr is not None:
        camino_inicio.append(curr)
        curr = visitados_inicio[curr] # Moverse al padre
    camino_inicio.reverse() # Invertir para [Inicio, ..., Encuentro]
    
    # 2. Camino desde NODO_ENCUENTRO -> OBJETIVO
    camino_objetivo = []
    curr = nodo_encuentro
    # Iteramos sobre los padres desde el objetivo (excluyendo el nodo de encuentro)
    curr = visitados_objetivo[curr] 
    while curr is not None:
        camino_objetivo.append(curr)
        curr = visitados_objetivo[curr] # Moverse al padre (en la búsqueda inversa)
        
    # 3. Combinar
    return camino_inicio + camino_objetivo


def busqueda_bidireccional(grafo, inicio, objetivo):
    """
    Encuentra el camino más corto usando BFS Bidireccional.
    """
    print(f"Iniciando Búsqueda Bidireccional (de {inicio} a {objetivo})...")

    # --- Configuración de la búsqueda HACIA ADELANTE ---
    cola_inicio = deque([inicio])
    # visitados_inicio guarda {nodo: padre}
    visitados_inicio = {inicio: None}

    # --- Configuración de la búsqueda HACIA ATRÁS ---
    cola_objetivo = deque([objetivo])
    # visitados_objetivo guarda {nodo: padre_inverso}
    visitados_objetivo = {objetivo: None}

    while cola_inicio and cola_objetivo:
        
        # --- 1. Expandir un paso desde INICIO ---
        if cola_inicio:
            nodo_actual_inicio = cola_inicio.popleft()
            print(f"  -> Visitando desde INICIO: {nodo_actual_inicio}")

            # 1a. Comprobar si se encontraron
            if nodo_actual_inicio in visitados_objetivo:
                print(f"¡Encuentro en {nodo_actual_inicio} (detectado por búsqueda INICIO)!")
                return reconstruir_camino(nodo_actual_inicio, visitados_inicio, visitados_objetivo)
            
            # 1b. Expandir vecinos
            for vecino in grafo.get(nodo_actual_inicio, []):
                if vecino not in visitados_inicio:
                    visitados_inicio[vecino] = nodo_actual_inicio
                    cola_inicio.append(vecino)

        # --- 2. Expandir un paso desde OBJETIVO ---
        if cola_objetivo:
            nodo_actual_objetivo = cola_objetivo.popleft()
            print(f"  <- Visitando desde OBJETIVO: {nodo_actual_objetivo}")

            # 2a. Comprobar si se encontraron
            if nodo_actual_objetivo in visitados_inicio:
                print(f"¡Encuentro en {nodo_actual_objetivo} (detectado por búsqueda OBJETIVO)!")
                return reconstruir_camino(nodo_actual_objetivo, visitados_inicio, visitados_objetivo)
            
            # 2b. Expandir vecinos (hacia atrás)
            # (En un grafo no dirigido, los vecinos son los mismos)
            for vecino in grafo.get(nodo_actual_objetivo, []):
                if vecino not in visitados_objetivo:
                    visitados_objetivo[vecino] = nodo_actual_objetivo
                    cola_objetivo.append(vecino)
    
    # Si una cola se vacía, no hay camino
    print("No se encontró camino (las búsquedas no se encontraron).")
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
print("\n--- 6. Búsqueda Bidireccional ---")
camino_bidireccional = busqueda_bidireccional(grafo_no_ponderado, 'A', 'F')
print(f"Camino encontrado: {camino_bidireccional}\n")

# Ejemplo a un nodo más lejano
camino_bidireccional_D = busqueda_bidireccional(grafo_no_ponderado, 'A', 'D')
print(f"Camino encontrado (A->D): {camino_bidireccional_D}\n")
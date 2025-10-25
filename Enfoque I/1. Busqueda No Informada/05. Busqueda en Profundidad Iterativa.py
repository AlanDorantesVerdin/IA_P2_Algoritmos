# Algoritmo 05. Búsqueda en Profundidad Iterativa
# Alan Dorantes Verdin

def busqueda_profundidad_iterativa(grafo, inicio, objetivo):
    """
    Llama a DLS en un bucle, incrementando el límite.
    """
    print(f"Iniciando IDS desde {inicio}...")
    
    limite = 0
    while True: # Bucle infinito hasta encontrarlo o agotar el grafo
        print(f"--- Probando con Límite: {limite} ---")
        
        # Usaremos una versión de DLS que devuelva un valor especial
        # si se cortó por el límite, para saber si debemos seguir iterando.
        
        # (Reutilizamos la lógica de DLS pero simplificada para IDS)
        def dls_para_ids(nodo_actual, profundidad, visitados):
            visitados.add(nodo_actual)
            
            if nodo_actual == objetivo:
                return ([nodo_actual], "encontrado") # (Camino, Estado)

            if profundidad >= limite:
                return (None, "limite_alcanzado") # (Camino, Estado)

            hubo_corte = False
            for vecino in grafo.get(nodo_actual, []):
                if vecino not in visitados:
                    (camino, estado) = dls_para_ids(vecino, profundidad + 1, visitados.copy())
                    
                    if estado == "encontrado":
                        return ([nodo_actual] + camino, "encontrado")
                    if estado == "limite_alcanzado":
                        hubo_corte = True
            
            # Si hubo cortes, "limite_alcanzado". Si no, "fallo" (rama muerta).
            return (None, "limite_alcanzado" if hubo_corte else "fallo")

        (camino_encontrado, estado_final) = dls_para_ids(inicio, 0, set())

        if estado_final == "encontrado":
            print(f"¡Objetivo {objetivo} encontrado en profundidad {limite}!")
            return camino_encontrado
        
        if estado_final == "fallo":
            # Si "fallo" es devuelto, significa que exploramos todo
            # y no se alcanzó ningún límite (el grafo es finito y no hay solución).
            print("Objetivo no encontrado (grafo explorado completamente).")
            return None
        
        # Si estado_final == "limite_alcanzado", incrementamos el límite y continuamos.
        limite += 1

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
print("\n--- 5. Búsqueda en Profundidad Iterativa (IDS) ---")
camino_ids = busqueda_profundidad_iterativa(grafo_no_ponderado, 'A', 'F')
print(f"Camino encontrado: {camino_ids}\n")
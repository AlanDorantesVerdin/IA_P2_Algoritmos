# Algoritmo 04. Búsqueda en Profundidad Limitada
# Alan Dorantes Verdin

def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    """
    DFS que se detiene en un 'limite' de profundidad.
    Usa recursión para manejar la profundidad fácilmente.
    """
    
    def dls_recursivo(nodo_actual, profundidad, visitados):
        print(f"Visitando: {nodo_actual} (Prof: {profundidad})")
        visitados.add(nodo_actual)

        # 1. Objetivo encontrado
        if nodo_actual == objetivo:
            return [nodo_actual] # Encontrado

        # 2. Límite de profundidad alcanzado
        if profundidad >= limite:
            return "limite_alcanzado" # Cortar búsqueda

        # 3. Explorar vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                # Llamada recursiva
                resultado = dls_recursivo(vecino, profundidad + 1, visitados.copy())
                
                if resultado == "limite_alcanzado":
                    # Si una rama falló por el límite, otras pueden tener éxito
                    continue 
                elif resultado is not None:
                    # Encontramos el objetivo en una rama hija
                    return [nodo_actual] + resultado

        return None # No encontrado en esta rama

    print(f"\nIniciando DLS desde {inicio} con límite {limite}...")
    resultado = dls_recursivo(inicio, 0, set())
    
    if resultado is None:
        print("Objetivo no encontrado.")
        return None
    elif resultado == "limite_alcanzado":
        print("Objetivo no encontrado (límite de profundidad alcanzado en todas las ramas).")
        return None
    else:
        print(f"¡Objetivo {objetivo} encontrado!")
        return resultado

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
print("\n--- 4. Búsqueda en Profundidad Limitada (DLS) ---")
# Con límite 2 (A->C->F), A->C es prof 1, C->F es prof 2.
camino_dls = busqueda_profundidad_limitada(grafo_no_ponderado, 'A', 'F', 2)
print(f"Camino encontrado (límite 2): {camino_dls}")
# Con límite 1 (No debería encontrarlo)
camino_dls_fallido = busqueda_profundidad_limitada(grafo_no_ponderado, 'A', 'F', 1)
print(f"Camino encontrado (límite 1): {camino_dls_fallido}\n")


import heapq

def busqueda_a_estrella(grafo, inicio, objetivo, h):
    """
    Encuentra el camino óptimo usando A*.
    f(n) = g(n) + h(n)
    g(n) = costo real desde el inicio hasta 'n'
    h(n) = heurística (costo estimado) desde 'n' hasta el objetivo
    """
    
    # 1. Cola de prioridad
    # Almacena: (f(n), g(n), nodo_actual, nodo_padre)
    # Se ordena por f(n)
    cola_prioridad = [(h(inicio), 0, inicio, None)] # g(inicio)=0, f(inicio)=h(inicio)
    
    # 2. Visitados (o 'cerrados')
    visitados = set()
    
    # 3. 'costos_g' almacena el mejor g(n) encontrado hasta ahora
    costos_g = {inicio: 0}
    
    # 4. Padres
    padres = {inicio: None}

    print(f"Iniciando A* desde {inicio}...")

    while cola_prioridad:
        
        # 5. Sacar el nodo con MENOR f(n)
        (f, g, nodo_actual, padre) = heapq.heappop(cola_prioridad)

        if nodo_actual in visitados:
            continue

        print(f"Visitando: {nodo_actual} (g={g}, h={h(nodo_actual)}, f={f})")
        visitados.add(nodo_actual)
        padres[nodo_actual] = padre

        # 6. Objetivo encontrado
        if nodo_actual == objetivo:
            print(f"¡Objetivo {objetivo} encontrado con costo {g}!")
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return (camino[::-1], g)

        # 7. Explorar vecinos
        for vecino, costo_arista in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                # Calculamos el nuevo costo g(vecino)
                nuevo_g = g + costo_arista
                
                # A* es óptimo si solo añadimos el camino si es mejor
                if vecino not in costos_g or nuevo_g < costos_g[vecino]:
                    costos_g[vecino] = nuevo_g
                    
                    # Calculamos f(vecino)
                    nuevo_f = nuevo_g + h(vecino)
                    
                    heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, vecino, nodo_actual))

    print(f"Objetivo {objetivo} no alcanzable.")
    return None

# Ejemplo de uso
print("--- 10. Búsqueda A* ---")
camino_a_estrella = busqueda_a_estrella(grafo_ponderado, 'A', 'F', h)
print(f"Camino encontrado: {camino_a_estrella}\n")
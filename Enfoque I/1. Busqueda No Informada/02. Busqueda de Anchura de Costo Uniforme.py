# -*- coding: utf-8 -*-
"""
Algoritmo 2: Búsqueda en Anchura de Costo Uniforme (UCS - Uniform Cost Search)

Descripción:
La Búsqueda de Costo Uniforme es un algoritmo de búsqueda en grafos que encuentra
el camino de menor costo desde un nodo inicial a un nodo objetivo. Es similar a BFS,
pero expande el nodo con el menor costo de camino acumulado (g(n)) primero.

Características Principales:
1.  Usa una Cola de Prioridad (Min-Heap) para gestionar los nodos pendientes
    de visitar. La prioridad de un nodo es el costo total del camino desde
    el inicio hasta ese nodo.
2.  Es "completo": siempre encontrará una solución si existe.
3.  Es "óptimo": siempre encontrará la solución de menor costo, siempre que
    los costos de las aristas no sean negativos (un requisito estándar).
4.  A diferencia de BFS, no explora nivel por nivel; explora en "ondas" de
    costo creciente.
5.  Es esencialmente el algoritmo de Dijkstra sin una heurística.
6.  Complejidad Temporal: O(b^(1 + C*/ε)), donde C* es el costo de la solución
    óptima y ε es el costo mínimo de una arista. También se expresa como
    O(E log V) o O(E + V log V) con implementaciones eficientes de heap.
7.  Complejidad Espacial: Similar a la temporal, ya que almacena todos los
    nodos en la frontera (la cola de prioridad).

"""

# Importamos 'heapq' para implementar la cola de prioridad (Priority Queue).
# heapq nos permite añadir elementos (heappush) y sacar el elemento
# con el valor (prioridad) más bajo (heappop) de forma eficiente (O(log N)).
import heapq

def busqueda_costo_uniforme(grafo, nodo_inicial, nodo_objetivo):
    """
    Implementación de la Búsqueda de Costo Uniforme (UCS).

    Argumentos:
    - grafo (dict): Un grafo ponderado. Es un diccionario donde cada clave
                    es un nodo y su valor es OTRO diccionario que mapea
                    nodos vecinos a sus costos.
                    Ej: {'A': {'B': 5, 'C': 1}, ...}
    - nodo_inicial (str/int): El nodo desde el cual comenzará la búsqueda.
    - nodo_objetivo (str/int): El nodo que estamos intentando alcanzar.

    Retorna:
    - Una tupla (costo_total, camino) si se encuentra el objetivo.
    - None si no se puede alcanzar el objetivo.
    """
    
    print(f"Iniciando Búsqueda de Costo Uniforme (UCS) de '{nodo_inicial}' a '{nodo_objetivo}'\n")

    # 1. 'cola_prioridad': Una lista que actuará como min-heap.
    #    Almacenaremos tuplas: (costo_acumulado, nodo_actual, camino_hasta_ahora)
    #    Empezamos con el nodo inicial, costo 0, y el camino inicial.
    cola_prioridad = [(0, nodo_inicial, [nodo_inicial])]
    
    # 2. 'visitados': Un conjunto (set) para llevar registro de los nodos
    #    para los cuales YA HEMOS ENCONTRADO el camino óptimo (el más barato).
    #    Esto es clave: un nodo solo se añade a 'visitados' cuando es
    #    *extraído* de la cola de prioridad, no cuando es añadido.
    visitados = set()

    # 3. Bucle principal: continuamos mientras la cola de prioridad no esté vacía.
    while cola_prioridad:
        
        # 4. Sacamos el nodo con el MENOR COSTO ACUMULADO de la cola.
        #    heapq.heappop() garantiza que obtiene el elemento con el primer
        #    valor de la tupla (el costo) más bajo.
        (costo_actual, nodo_actual, camino_actual) = heapq.heappop(cola_prioridad)
        
        print(f"Evaluando: {nodo_actual} (Costo: {costo_actual})")

        # 5. Comprobación de nodo visitado:
        #    Si ya hemos sacado este nodo de la cola antes, significa que
        #    ya encontramos un camino más barato (o igual) hacia él. Lo ignoramos.
        if nodo_actual in visitados:
            print(f"  -> '{nodo_actual}' ya fue visitado con un costo óptimo. Omitiendo.")
            continue

        # 6. Marcar como visitado (procesado).
        #    Ahora declaramos que el camino actual a 'nodo_actual' es el óptimo.
        visitados.add(nodo_actual)

        # 7. ¡Comprobación del objetivo!
        #    Si el nodo que sacamos es el objetivo, hemos terminado.
        #    Debido a la naturaleza de la cola de prioridad, la primera vez
        #    que sacamos el nodo objetivo, garantizamos que es por el
        #    camino de menor costo.
        if nodo_actual == nodo_objetivo:
            print(f"\n¡Objetivo '{nodo_objetivo}' alcanzado!")
            return costo_actual, camino_actual

        # 8. Explorar vecinos.
        #    Iteramos sobre los vecinos del nodo actual y el costo de la arista
        #    para llegar a ellos.
        for vecino, costo_arista in grafo.get(nodo_actual, {}).items():
            
            # 9. Si el vecino no ha sido procesado (visitado) aún...
            if vecino not in visitados:
                
                # 10. Calculamos el nuevo costo acumulado para llegar a ese vecino.
                nuevo_costo = costo_actual + costo_arista
                
                # 11. Creamos el nuevo camino.
                nuevo_camino = camino_actual + [vecino]
                
                # 12. Añadimos el vecino a la cola de prioridad con su nuevo
                #     costo y camino. heapq.heappush() lo ordenará
                #     automáticamente.
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino, nuevo_camino))
                print(f"  -> Encolando vecino: {vecino} (Costo total: {nuevo_costo})")
    
    # 13. Si el bucle termina y no encontramos el objetivo, no hay camino.
    print(f"\nNo se pudo encontrar un camino de '{nodo_inicial}' a '{nodo_objetivo}'.")
    return None

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    
    # Definimos un grafo ponderado.
    # Los números representan el "costo" de viajar entre nodos.
    #
    #      (5) ---  B - (3) - D
    #    /  |       |         |
    #   /  (9)     (1)       (4)
    #  /    |       |         |
    # A  - (2)  -   C - (8) - F
    #  \          
    #    - (15)  -  E 
    
    mi_grafo_ponderado = {
        'A': {'B': 5, 'C': 2, 'E': 15},
        'B': {'A': 5, 'C': 1, 'D': 3},
        'C': {'A': 2, 'B': 1, 'F': 8},
        'D': {'B': 3, 'F': 4},
        'E': {'A': 15},
        'F': {'C': 8, 'D': 4}
    }

    nodo_inicio = 'A'
    nodo_fin = 'F'
    
    resultado = busqueda_costo_uniforme(mi_grafo_ponderado, nodo_inicio, nodo_fin)
    
    if resultado:
        costo_optimo, camino_optimo = resultado
        print("\n--- Resultado Final ---")
        print(f"Camino más corto de '{nodo_inicio}' a '{nodo_fin}': {' -> '.join(camino_optimo)}")
        print(f"Costo total del camino: {costo_optimo}")

    # Nota: El camino A->C->F tiene costo 2+8=10.
    # El camino A->B->D->F tiene costo 5+3+4=12.
    # El camino A->C->B->D->F tiene costo 2+1+3+4=10.
    # UCS encontrará uno de los caminos óptimos (en este caso, hay dos con costo 10).
    # La salida exacta del camino puede ser A->C->F o A->C->B->D->F dependiendo
    # de cómo se resuelvan los empates en la cola de prioridad.

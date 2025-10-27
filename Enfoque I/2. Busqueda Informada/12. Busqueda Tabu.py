# Algoritmo 12. Búsqueda Tabú
# Alan Dorantes Verdin

from collections import deque
import random

LONGITUD_ESTADO = 10 # Ej. '1011001010'

def crear_estado_aleatorio():
    """ Crea un string binario aleatorio """
    return "".join(random.choice(['0', '1']) for _ in range(LONGITUD_ESTADO))

def fitness(estado):
    """ Función de evaluación (heurística): cuenta el número de '1's """
    return estado.count('1')

def get_vecino_aleatorio(estado):
    """ Muta un bit aleatorio del estado para obtener un vecino """
    indice = random.randint(0, LONGITUD_ESTADO - 1)
    nuevo_bit = '1' if estado[indice] == '0' else '0'
    
    lista_estado = list(estado)
    lista_estado[indice] = nuevo_bit
    return "".join(lista_estado)

print(f"\n--- Configuración para Búsqueda Local (Problema One-Max, Long={LONGITUD_ESTADO}) ---")
estado_test = crear_estado_aleatorio()
print(f"Estado de prueba: {estado_test}, Fitness: {fitness(estado_test)}")
print(f"Vecino aleatorio: {get_vecino_aleatorio(estado_test)}\n")

def busqueda_tabu(max_iteraciones, tamano_tabu):
    """
    Hill Climbing con una lista tabú para evitar ciclos cortos.
    """
    # 1. Lista Tabú (guarda los últimos 'tamano_tabu' estados)
    lista_tabu = deque(maxlen=tamano_tabu)
    
    estado_actual = crear_estado_aleatorio()
    fitness_actual = fitness(estado_actual)
    
    # Guardamos el mejor estado visto en general
    mejor_estado_global = estado_actual
    mejor_fitness_global = fitness_actual
    
    print(f"Iniciando Búsqueda Tabú. Inicial: {estado_actual} (Fitness: {fitness_actual})")
    
    for i in range(max_iteraciones):
        # 2. Generar varios vecinos (en lugar de solo 1)
        mejor_vecino = None
        mejor_fitness_vecino = -1

        # (Simplicidad: solo probamos 5 vecinos aleatorios)
        for _ in range(5): 
            vecino = get_vecino_aleatorio(estado_actual)
            
            # 3. Criterio de aspiración:
            # El vecino NO debe estar en la lista tabú...
            if (vecino not in lista_tabu):
                f_vecino = fitness(vecino)
                if f_vecino > mejor_fitness_vecino:
                    mejor_vecino = vecino
                    mejor_fitness_vecino = f_vecino

        if mejor_vecino is None:
            # Si todos los vecinos están en la lista tabú, nos movemos 
            # al primero que generemos (para no atascarnos)
            mejor_vecino = get_vecino_aleatorio(estado_actual)
            mejor_fitness_vecino = fitness(mejor_vecino)
            
        # 4. Moverse al mejor vecino (incluso si es peor que el actual)
        estado_actual = mejor_vecino
        fitness_actual = mejor_fitness_vecino
        
        # 5. Añadir el nuevo estado a la lista tabú
        lista_tabu.append(estado_actual)
        
        # 6. Actualizar el mejor global
        if fitness_actual > mejor_fitness_global:
            mejor_estado_global = estado_actual
            mejor_fitness_global = fitness_actual
            print(f"Iter {i}: Nuevo mejor global {mejor_estado_global} (Fitness: {mejor_fitness_global})")
            
        if mejor_fitness_global == LONGITUD_ESTADO:
            print("¡Óptimo global encontrado!")
            break

    print(f"Búsqueda finalizada. Mejor estado: {mejor_estado_global}, Fitness: {mejor_fitness_global}")
    return mejor_estado_global

# Ejemplo de uso
print("\n--- 12. Búsqueda Tabú ---")
mejor_estado_tabu = busqueda_tabu(max_iteraciones=100, tamano_tabu=5)
print(f"Mejor estado encontrado: {mejor_estado_tabu}\n")
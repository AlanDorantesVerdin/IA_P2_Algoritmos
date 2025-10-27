# Algoritmo 11. Búsqueda de Ascensión de Colinas
# Alan Dorantes Verdin

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

def ascension_colinas(max_iteraciones):
    """
    Intenta maximizar el fitness (número de '1's) usando Hill Climbing.
    """
    # 1. Empezar en un estado aleatorio
    estado_actual = crear_estado_aleatorio()
    fitness_actual = fitness(estado_actual)
    
    print(f"Iniciando Hill Climbing. Estado inicial: {estado_actual} (Fitness: {fitness_actual})")

    for i in range(max_iteraciones):
        # 2. Evaluar un vecino aleatorio
        vecino = get_vecino_aleatorio(estado_actual)
        fitness_vecino = fitness(vecino)

        # 3. Moverse solo si el vecino es MEJOR
        if fitness_vecino > fitness_actual:
            estado_actual = vecino
            fitness_actual = fitness_vecino
            print(f"Iter {i}: Moviendo a {estado_actual} (Fitness: {fitness_actual})")

        # 4. Condición de parada (Óptimo global encontrado)
        if fitness_actual == LONGITUD_ESTADO:
            print("¡Óptimo global encontrado!")
            break
            
        # Si no mejora, se queda quieto (en este ejemplo, podría intentarlo
        # de nuevo en la siguiente iteración). Si ningún vecino es mejor,
        # se dice que está en un "óptimo local".

    print(f"Búsqueda finalizada. Mejor estado: {estado_actual}, Fitness: {fitness_actual}")
    return estado_actual

# Ejemplo de uso
print("\n--- 11. Búsqueda de Ascensión de Colinas ---")
mejor_estado_hc = ascension_colinas(max_iteraciones=100)
print(f"Mejor estado encontrado: {mejor_estado_hc}\n")
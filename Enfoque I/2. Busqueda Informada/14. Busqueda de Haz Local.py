# Algoritmo 14. Búsqueda de Haz Local
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

def busqueda_haz_local(k, max_iteraciones):
    """
    Mantiene k estados (el haz) y explora sus vecinos.
    """
    
    # 1. Generar k estados iniciales aleatorios (el haz)
    haz = [crear_estado_aleatorio() for _ in range(k)]
    
    print(f"Iniciando Búsqueda de Haz Local (k={k}).")
    
    for i in range(max_iteraciones):
        
        # 2. Generar TODOS los vecinos de TODOS los estados en el haz
        # (Para simplicidad, generaremos solo k*2 vecinos aleatorios en total)
        vecinos_candidatos = []
        for estado in haz:
            # (Una implementación real generaría TODOS los vecinos)
            vecinos_candidatos.append(get_vecino_aleatorio(estado))
            vecinos_candidatos.append(get_vecino_aleatorio(estado))

        # 3. Evaluar a todos los candidatos (incluyendo el haz actual)
        todos_candidatos = haz + vecinos_candidatos
        
        # 4. Ordenar por fitness (de mejor a peor)
        candidatos_ordenados = sorted(todos_candidatos, key=fitness, reverse=True)
        
        # 5. El nuevo haz son los k mejores
        haz = candidatos_ordenados[:k]
        
        mejor_fitness_actual = fitness(haz[0])
        print(f"Iter {i}: Mejor fitness en el haz: {mejor_fitness_actual}")

        if mejor_fitness_actual == LONGITUD_ESTADO:
            print("¡Óptimo global encontrado!")
            break
            
    print(f"Búsqueda finalizada. Mejor estado: {haz[0]}, Fitness: {fitness(haz[0])}")
    return haz[0]

# Ejemplo de uso
print("\n--- 14. Búsqueda de Haz Local ---")
mejor_estado_beam = busqueda_haz_local(k=3, max_iteraciones=50)
print(f"Mejor estado encontrado: {mejor_estado_beam}\n")
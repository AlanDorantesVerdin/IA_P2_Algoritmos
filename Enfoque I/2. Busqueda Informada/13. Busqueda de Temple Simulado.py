# Algoritmo 13. Búsqueda de Temple Simulado
# Alan Dorantes Verdin

import math
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

def temple_simulado(temp_inicial, factor_enfriamiento):
    """
    Búsqueda que acepta malos movimientos basado en una 'temperatura'.
    """
    estado_actual = crear_estado_aleatorio()
    fitness_actual = fitness(estado_actual)
    
    mejor_estado = estado_actual
    mejor_fitness = fitness_actual
    
    temperatura = temp_inicial
    
    print(f"Iniciando Temple Simulado. Inicial: {estado_actual} (Fitness: {fitness_actual})")

    iteracion = 0
    while temperatura > 0.01 and mejor_fitness < LONGITUD_ESTADO:
        
        # 1. Generar un vecino aleatorio
        vecino = get_vecino_aleatorio(estado_actual)
        fitness_vecino = fitness(vecino)
        
        # 2. Calcular la diferencia de energía (delta E)
        # Como queremos MAXIMIZAR, invertimos el signo
        delta_fitness = fitness_vecino - fitness_actual

        # 3. Decidir si moverse
        if delta_fitness > 0:
            # Movimiento bueno (cuesta arriba), siempre se acepta
            estado_actual = vecino
            fitness_actual = fitness_vecino
        else:
            # Movimiento malo (cuesta abajo)
            # Calcular probabilidad de aceptación
            probabilidad = math.exp(delta_fitness / temperatura)
            
            if random.random() < probabilidad:
                # Aceptar el movimiento malo
                estado_actual = vecino
                fitness_actual = fitness_vecino
                print(f"Iter {iteracion}: Aceptando movimiento MALO (Temp: {temperatura:.2f})")

        # 4. Actualizar el mejor global
        if fitness_actual > mejor_fitness:
            mejor_estado = estado_actual
            mejor_fitness = fitness_actual
            print(f"Iter {iteracion}: Nuevo mejor {mejor_estado} (Fitness: {mejor_fitness})")

        # 5. Enfriar la temperatura
        temperatura *= factor_enfriamiento
        iteracion += 1

    print(f"Búsqueda finalizada. Mejor estado: {mejor_estado}, Fitness: {mejor_fitness}")
    return mejor_estado

# Ejemplo de uso
print("\n--- 13. Búsqueda de Temple Simulado ---")
mejor_estado_sa = temple_simulado(temp_inicial=10.0, factor_enfriamiento=0.99)
print(f"Mejor estado encontrado: {mejor_estado_sa}\n")
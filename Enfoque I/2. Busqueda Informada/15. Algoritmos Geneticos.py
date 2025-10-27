# Algoritmo 15. Algoritmos Genéticos
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

# --- Funciones nuevas para AG ---

def seleccion(poblacion, k=2):
    """ Selecciona 'k' individuos usando 'selección por torneo' """
    seleccionados = []
    for _ in range(k):
        # Tomar 2 padres al azar
        padre1 = random.choice(poblacion)
        padre2 = random.choice(poblacion)
        # El que tenga mejor fitness 'gana' el torneo
        if fitness(padre1) > fitness(padre2):
            seleccionados.append(padre1)
        else:
            seleccionados.append(padre2)
    return seleccionados[0], seleccionados[1] # Devolver 2 padres

def cruce(padre1, padre2):
    """ Cruce de un solo punto """
    punto_cruce = random.randint(1, LONGITUD_ESTADO - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

def mutacion(individuo, tasa_mutacion):
    """ Invierte bits aleatoriamente basado en la tasa de mutación """
    lista_individuo = list(individuo)
    for i in range(LONGITUD_ESTADO):
        if random.random() < tasa_mutacion:
            # Invertir el bit
            lista_individuo[i] = '1' if individuo[i] == '0' else '0'
    return "".join(lista_individuo)

# --- Algoritmo Principal ---

def algoritmo_genetico(tam_poblacion, generaciones, tasa_mutacion):
    
    print(f"Iniciando Algoritmo Genético (Pob={tam_poblacion}, Gen={generaciones})")
    
    # 1. Inicializar Población
    poblacion = [crear_estado_aleatorio() for _ in range(tam_poblacion)]
    
    mejor_global = poblacion[0]
    mejor_fitness_global = fitness(mejor_global)

    for gen in range(generaciones):
        
        nueva_poblacion = []
        
        while len(nueva_poblacion) < tam_poblacion:
            # 2. Selección
            padre1, padre2 = seleccion(poblacion)
            
            # 3. Cruce
            hijo1, hijo2 = cruce(padre1, padre2)
            
            # 4. Mutación
            hijo1 = mutacion(hijo1, tasa_mutacion)
            hijo2 = mutacion(hijo2, tasa_mutacion)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        # 5. Nueva generación
        poblacion = nueva_poblacion
        
        # 6. Evaluar
        mejor_actual = max(poblacion, key=fitness)
        fitness_actual = fitness(mejor_actual)
        
        if fitness_actual > mejor_fitness_global:
            mejor_global = mejor_actual
            mejor_fitness_global = fitness_actual
            print(f"Gen {gen}: Nuevo mejor {mejor_global} (Fitness: {mejor_fitness_global})")
        
        if mejor_fitness_global == LONGITUD_ESTADO:
            print("¡Óptimo global encontrado!")
            break
            
    print(f"Búsqueda finalizada. Mejor estado: {mejor_global}, Fitness: {mejor_fitness_global}")
    return mejor_global

# Ejemplo de uso
print("\n--- 15. Algoritmos Genéticos ---")
mejor_estado_ag = algoritmo_genetico(tam_poblacion=20, generaciones=100, tasa_mutacion=0.01)
print(f"Mejor estado encontrado: {mejor_estado_ag}\n")
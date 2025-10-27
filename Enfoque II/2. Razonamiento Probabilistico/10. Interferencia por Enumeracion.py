# Algoritmo 10. Interferencia por Enumeración
# Alan Dorantes Verdin

print("\n--- 10. Interferencia por Enumeración ---")

# Requerimos la 'red_bayesiana' y sus CPTs del subtema 7.

# Las Tablas de Probabilidad Condicionada (CPTs) definen la red.
# Usamos diccionarios anidados.
# Las claves 'T' y 'F' significan True (Verdadero) y False (Falso).

# P(N)
cpt_nublado = {
    'T': 0.5,
    'F': 0.5
}

# P(A | N)
cpt_aspersor = {
    'T': {'T': 0.1, 'F': 0.9},  # P(A | N=T)
    'F': {'T': 0.5, 'F': 0.5}   # P(A | N=F)
}

# P(L | N)
cpt_lluvia = {
    'T': {'T': 0.8, 'F': 0.2},  # P(L | N=T)
    'F': {'T': 0.2, 'F': 0.8}   # P(L | N=F)
}

# P(PM | A, L)
cpt_pasto_mojado = {
    ('T', 'T'): {'T': 0.99, 'F': 0.01}, # P(PM | A=T, L=T)
    ('T', 'F'): {'T': 0.9, 'F': 0.1},  # P(PM | A=T, L=F)
    ('F', 'T'): {'T': 0.9, 'F': 0.1},  # P(PM | A=F, L=T)
    ('F', 'F'): {'T': 0.0, 'F': 1.0}   # P(PM | A=F, L=F)
}

# Juntamos la red en un solo diccionario para fácil acceso
red_bayesiana = {
    'N': cpt_nublado,
    'A': cpt_aspersor,
    'L': cpt_lluvia,
    'PM': cpt_pasto_mojado
}


def enumeracion_ask(variable_X, evidencia_e, variables_red):
    """
    Calcula P(X | e) usando enumeración.
    - variable_X: El nombre del nodo a consultar (ej. 'L')
    - evidencia_e: Un diccionario de nodos con valor fijo (ej. {'PM': 'T'})
    - variables_red: Una lista de TODOS los nodos en orden topológico
    """
    # Q es la distribución de probabilidad para X
    Q = {}
    for valor_x in ['T', 'F']:
        # Copiamos la evidencia y añadimos el valor actual de X
        evidencia_extendida = evidencia_e.copy()
        evidencia_extendida[variable_X] = valor_x
        
        # Llamamos a la función recursiva que suma sobre las variables ocultas
        Q[valor_x] = enumeracion_todos(variables_red, evidencia_extendida)
        
    # Normalizamos para que la suma de Q sea 1
    return normalizar(Q)

def enumeracion_todos(variables, evidencia):
    """
    Función recursiva que calcula la suma de probabilidades.
    """
    if not variables:
        return 1.0
        
    Y, resto_variables = variables[0], variables[1:]
    
    if Y in evidencia:
        # Si Y está en la evidencia, su valor está fijo
        valor_Y = evidencia[Y]
        
        # Obtenemos P(Y | Padres(Y))
        prob_Y = calcular_prob_nodo(Y, valor_Y, evidencia)
        
        return prob_Y * enumeracion_todos(resto_variables, evidencia)
    else:
        # Si Y no está en la evidencia (es oculta), sumamos sobre sus valores
        suma = 0
        for valor_Y in ['T', 'F']:
            evidencia_extendida = evidencia.copy()
            evidencia_extendida[Y] = valor_Y
            
            # Obtenemos P(Y | Padres(Y))
            prob_Y = calcular_prob_nodo(Y, valor_Y, evidencia_extendida)
            
            suma += prob_Y * enumeracion_todos(resto_variables, evidencia_extendida)
        return suma

def calcular_prob_nodo(Y, valor_Y, evidencia):
    """
    Calcula P(Y=valor_Y | Padres(Y)) usando las CPTs
    """
    if Y == 'N':
        return red_bayesiana['N'][valor_Y]
    elif Y == 'A':
        padre_N = evidencia['N']
        return red_bayesiana['A'][padre_N][valor_Y]
    elif Y == 'L':
        padre_N = evidencia['N']
        return red_bayesiana['L'][padre_N][valor_Y]
    elif Y == 'PM':
        padre_A = evidencia['A']
        padre_L = evidencia['L']
        return red_bayesiana['PM'][(padre_A, padre_L)][valor_Y]
    return 0

def normalizar(Q):
    """
    Convierte {T: 0.1, F: 0.3} en {T: 0.25, F: 0.75}
    """
    suma_total = sum(Q.values())
    if suma_total == 0:
        return Q
    for clave in Q:
        Q[clave] = Q[clave] / suma_total
    return Q

# --- Ejemplo de Consulta ---
# ¿Cuál es la probabilidad de Lluvia ('L'), dado que el Pasto está Mojado ('PM'=T)?
variables_ordenadas = ['N', 'A', 'L', 'PM'] # Orden topológico
evidencia = {'PM': 'T'}
consulta = 'L'

distribucion_L = enumeracion_ask(consulta, evidencia, variables_ordenadas)
print(f"Consulta: P(L | PM=T) = {distribucion_L}")
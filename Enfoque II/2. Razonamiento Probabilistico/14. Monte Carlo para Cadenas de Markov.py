# Algoritmo 14. Monte Carlo para Cadenas de Markov
# Alan Dorantes Verdin

print("\n--- 14. Monte Carlo para Cadenas de Markov ---")

import random

# Requerimos la 'red_bayesiana' del subtema 7

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

def muestreo_gibbs(variable_X, evidencia_e, N_muestras, N_calentamiento):
    """
    Calcula P(X='T' | e) usando Muestreo de Gibbs.
    """
    
    # 1. Inicializar estado
    # Empezamos con la evidencia fija
    estado = evidencia_e.copy()
    
    # Obtenemos las variables ocultas
    variables_ocultas = []
    for var in ['N', 'A', 'L', 'PM']:
        if var not in evidencia_e:
            variables_ocultas.append(var)
            # Inicializamos al azar
            estado[var] = 'T' if random.random() < 0.5 else 'F'
            
    if not variables_ocultas:
        print("Error: No hay variables ocultas para muestrear.")
        return 0

    contador_X = 0
    total_muestras_post_calentamiento = N_muestras - N_calentamiento
    
    # 3. Bucle de muestreo
    for i in range(N_muestras):
        # Elegimos una variable oculta al azar para actualizar
        Y_i = random.choice(variables_ocultas)
        
        # 4. Volver a muestrear Y_i dado su Manto de Markov
        estado = re_muestrear_variable(Y_i, estado)
        
        # 5. Contar después del calentamiento
        if i >= N_calentamiento:
            if estado[variable_X] == 'T':
                contador_X += 1
                
    return contador_X / total_muestras_post_calentamiento


def re_muestrear_variable(Y_i, estado_actual):
    """
    Función de ayuda para Gibbs: Muestrea Y_i | Manto(Y_i)
    """
    
    # P(Y_i | Manto) es proporcional a P(Y_i | Padres) * Producto( P(Hijo_j | Padres_j) )
    # Calculamos la prob NO normalizada para Y_i=T y Y_i=F
    
    # Probabilidad para Y_i = 'T'
    estado_T = estado_actual.copy()
    estado_T[Y_i] = 'T'
    prob_T = calcular_prob_con_manto(Y_i, estado_T)
    
    # Probabilidad para Y_i = 'F'
    estado_F = estado_actual.copy()
    estado_F[Y_i] = 'F'
    prob_F = calcular_prob_con_manto(Y_i, estado_F)
    
    # Normalizar
    norm = prob_T + prob_F
    if norm == 0:
        prob_T_norm = 0.5
    else:
        prob_T_norm = prob_T / norm
        
    # Muestrear
    nuevo_estado = estado_actual.copy()
    if random.random() < prob_T_norm:
        nuevo_estado[Y_i] = 'T'
    else:
        nuevo_estado[Y_i] = 'F'
        
    return nuevo_estado

def calcular_prob_con_manto(Y_i, estado):
    """
    Calcula P(Y_i | Padres(Y_i)) * Producto P(Hijos | Padres(Hijos))
    """
    # 1. P(Y_i | Padres(Y_i))
    if Y_i == 'N':
        prob = red_bayesiana['N'][estado['N']]
    elif Y_i == 'A':
        prob = red_bayesiana['A'][estado['N']][estado['A']]
    elif Y_i == 'L':
        prob = red_bayesiana['L'][estado['N']][estado['L']]
    elif Y_i == 'PM':
        prob = red_bayesiana['PM'][(estado['A'], estado['L'])][estado['PM']]

    # 2. Multiplicar por P(Hijos | Padres)
    if Y_i == 'N': # Hijos: A, L
        prob *= red_bayesiana['A'][estado['N']][estado['A']]
        prob *= red_bayesiana['L'][estado['N']][estado['L']]
    elif Y_i == 'A': # Hijo: PM
        prob *= red_bayesiana['PM'][(estado['A'], estado['L'])][estado['PM']]
    elif Y_i == 'L': # Hijo: PM
        prob *= red_bayesiana['PM'][(estado['A'], estado['L'])][estado['PM']]
    # PM no tiene hijos, así que no se multiplica nada más
    
    return prob

# --- Ejemplo de Consulta ---
# P(L='T' | PM='T')?
N_muestras_gibbs = 10000
N_calentamiento_gibbs = 1000
evidencia = {'PM': 'T'}
consulta = 'L'

prob_gibbs = muestreo_gibbs(consulta, evidencia, N_muestras_gibbs, N_calentamiento_gibbs)
print(f"--- Muestreo de Gibbs (MCMC) (N={N_muestras_gibbs}) ---")
print(f"Consulta: P(L='T' | PM='T') ≈ {prob_gibbs:.5f}")
# (Debería ser similar a los otros resultados)
# Algoritmo 8. Regla de la Cadena
# Alan Dorantes Verdin

print("\n--- 8. Regla de la Cadena ---")

# Requerimos la 'red_bayesiana' definida en el subtema 7. Red Bayesiana
# Reutilizamos las tablas de probabilidad condicionada (CPTs)
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

def calcular_prob_conjunta(n, a, l, pm):
    """
    Calcula la probabilidad conjunta P(N, A, L, PM)
    usando la regla de la cadena de la red bayesiana.
    Los argumentos n, a, l, pm deben ser 'T' o 'F'.
    """
    
    # P(N)
    p_n = red_bayesiana['N'][n]
    
    # P(A | N)
    p_a_dado_n = red_bayesiana['A'][n][a]
    
    # P(L | N)
    p_l_dado_n = red_bayesiana['L'][n][l]
    
    # P(PM | A, L)
    p_pm_dado_a_l = red_bayesiana['PM'][(a, l)][pm]
    
    # Multiplicar todo
    probabilidad_total = p_n * p_a_dado_n * p_l_dado_n * p_pm_dado_a_l
    
    return probabilidad_total

# Ejemplo: ¿Cuál es la probabilidad de que esté nublado (T), 
# no haya aspersor (F), llueva (T) y el pasto esté mojado (T)?
prob = calcular_prob_conjunta('T', 'F', 'T', 'T')

print(f"P(N=T, A=F, L=T, PM=T) = {prob:.5f}")
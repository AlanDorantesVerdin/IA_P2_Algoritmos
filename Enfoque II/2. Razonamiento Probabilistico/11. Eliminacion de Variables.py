# Algoritmo 11. Eliminación de Variables
# Alan Dorantes Verdin

print("\n--- 11. Eliminación de Variables ---")

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

def eliminacion_variables_simple(valor_pm):
    """
    Calcula P(PM) usando el principio de eliminación de variables
    (implementado manualmente para esta red específica).
    """
    suma_total = 0
    
    # Bucle externo: \sum_N P(N) ...
    for valor_n in ['T', 'F']:
        p_n = red_bayesiana['N'][valor_n]
        
        suma_dado_n = 0
        
        # Bucle medio: \sum_A P(A|N) ...
        for valor_a in ['T', 'F']:
            p_a_dado_n = red_bayesiana['A'][valor_n][valor_a]
            
            suma_dado_n_a = 0
            
            # Bucle interno: \sum_L P(L|N) * P(PM|A,L)
            for valor_l in ['T', 'F']:
                p_l_dado_n = red_bayesiana['L'][valor_n][valor_l]
                p_pm_dado_a_l = red_bayesiana['PM'][(valor_a, valor_l)][valor_pm]
                
                suma_dado_n_a += p_l_dado_n * p_pm_dado_a_l
            
            # Multiplicamos el resultado de la suma interna (Factor(A, PM))
            suma_dado_n += p_a_dado_n * suma_dado_n_a
            
        # Multiplicamos el resultado de la suma media (Factor(N, PM))
        suma_total += p_n * suma_dado_n
        
    return suma_total

# Calculamos P(PM='T')
prob_pm_T = eliminacion_variables_simple('T')
print(f"Cálculo de P(PM=T) usando Eliminación de Variables (conceptual): {prob_pm_T:.5f}")

# Podemos verificar P(PM='F') y ver que suman 1
prob_pm_F = eliminacion_variables_simple('F')
print(f"Cálculo de P(PM=F) usando Eliminación de Variables (conceptual): {prob_pm_F:.5f}")
print(f"Suma (Normalización): {prob_pm_T + prob_pm_F}")
# Algoritmo 13. Ponderación de Verosimilitud
# Alan Dorantes Verdin

print("\n--- 13. Ponderación de Verosimilitud ---")

import random

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

def ponderacion_de_verosimilitud_muestra(evidencia_e):
    """
    Genera una única muestra ponderada (muestra, peso).
    """
    muestra = {} # La muestra que estamos construyendo
    peso = 1.0
    
    # Iteramos en orden topológico ('N', 'A', 'L', 'PM')
    
    # 1. Muestrear/Ponderar N
    if 'N' in evidencia_e:
        valor_n = evidencia_e['N']
        peso *= red_bayesiana['N'][valor_n] # Ponderar
    else:
        valor_n = 'T' if random.random() < red_bayesiana['N']['T'] else 'F'
    muestra['N'] = valor_n
    
    # 2. Muestrear/Ponderar A
    if 'A' in evidencia_e:
        valor_a = evidencia_e['A']
        peso *= red_bayesiana['A'][valor_n][valor_a] # Ponderar
    else:
        prob_a_T = red_bayesiana['A'][valor_n]['T']
        valor_a = 'T' if random.random() < prob_a_T else 'F'
    muestra['A'] = valor_a
        
    # 3. Muestrear/Ponderar L
    if 'L' in evidencia_e:
        valor_l = evidencia_e['L']
        peso *= red_bayesiana['L'][valor_n][valor_l] # Ponderar
    else:
        prob_l_T = red_bayesiana['L'][valor_n]['T']
        valor_l = 'T' if random.random() < prob_l_T else 'F'
    muestra['L'] = valor_l
    
    # 4. Muestrear/Ponderar PM
    if 'PM' in evidencia_e:
        valor_pm = evidencia_e['PM']
        peso *= red_bayesiana['PM'][(valor_a, valor_l)][valor_pm] # Ponderar
    else:
        prob_pm_T = red_bayesiana['PM'][(valor_a, valor_l)]['T']
        valor_pm = 'T' if random.random() < prob_pm_T else 'F'
    muestra['PM'] = valor_pm

    return muestra, peso

def algoritmo_ponderacion_verosimilitud(variable_X, valor_X, evidencia_e, N_muestras):
    """
    Calcula P(X=valor_X | e) usando Ponderación de Verosimilitud.
    """
    suma_total_pesos = 0
    suma_pesos_X = 0
    
    for _ in range(N_muestras):
        muestra, peso = ponderacion_de_verosimilitud_muestra(evidencia_e)
        
        suma_total_pesos += peso
        
        if muestra[variable_X] == valor_X:
            suma_pesos_X += peso
            
    if suma_total_pesos == 0:
        return 0
        
    return suma_pesos_X / suma_total_pesos

# --- Ejemplo de Consulta ---
# P(L='T' | PM='T')?
N = 100000
evidencia = {'PM': 'T'}
consulta = 'L'
valor_consulta = 'T'

prob_pond = algoritmo_ponderacion_verosimilitud(consulta, valor_consulta, evidencia, N)
print(f"--- Ponderación de Verosimilitud (N={N}) ---")
print(f"Consulta: P(L='T' | PM='T') ≈ {prob_pond:.5f}")
# (Este resultado converge mucho más rápido y es más estable que el rechazo)
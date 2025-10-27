# Algoritmo 12. Muestreo Directo y por Rechazo
# Alan Dorantes Verdin

print("\n--- 12. Muestreo Directo y por Rechazo ---")

# Requerimos la 'red_bayesiana' del subtema 7

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

import random

def muestreo_directo():
    """
    Genera una única muestra completa de la red.
    """
    # 1. Muestrear N
    valor_n = 'T' if random.random() < red_bayesiana['N']['T'] else 'F'
    
    # 2. Muestrear A (dado N)
    prob_a_T = red_bayesiana['A'][valor_n]['T']
    valor_a = 'T' if random.random() < prob_a_T else 'F'
    
    # 3. Muestrear L (dado N)
    prob_l_T = red_bayesiana['L'][valor_n]['T']
    valor_l = 'T' if random.random() < prob_l_T else 'F'
    
    # 4. Muestrear PM (dado A, L)
    prob_pm_T = red_bayesiana['PM'][(valor_a, valor_l)]['T']
    valor_pm = 'T' if random.random() < prob_pm_T else 'F'
    
    # Devolver la muestra como un diccionario
    return {'N': valor_n, 'A': valor_a, 'L': valor_l, 'PM': valor_pm}

def muestreo_por_rechazo(variable_X, evidencia_e, N_muestras):
    """
    Calcula P(X | e) usando Muestreo por Rechazo.
    """
    contador_evidencia = 0 # Contador para muestras que coinciden con 'e'
    contador_X_y_evidencia = 0 # Contador para muestras que coinciden con 'X' y 'e'
    
    for _ in range(N_muestras):
        # 1. Generar una muestra
        muestra = muestreo_directo()
        
        # 2. Verificar si coincide con la evidencia
        coincide_evidencia = True
        for var, val in evidencia_e.items():
            if muestra[var] != val:
                coincide_evidencia = False
                break
        
        # 3. Si no coincide, se RECHAZA la muestra
        if not coincide_evidencia:
            continue
            
        # 4. Si coincide, la aceptamos
        contador_evidencia += 1
        
        # 5. Verificamos si también coincide con la variable X que consultamos
        # (Asumimos que X es una sola variable con valor 'T')
        if muestra[variable_X] == 'T': 
            contador_X_y_evidencia += 1
            
    # 6. Calcular la probabilidad
    if contador_evidencia == 0:
        return 0.0 # No se encontraron muestras que coincidan con la evidencia
        
    return contador_X_y_evidencia / contador_evidencia

# --- Ejemplo de Consulta ---
# P(L='T' | PM='T')? (La misma consulta que en Enumeración)
N = 100000
evidencia = {'PM': 'T'}
consulta = 'L' # Buscamos P(L='T' | ...)

prob_rechazo = muestreo_por_rechazo(consulta, evidencia, N)
print(f"\n--- Muestreo por Rechazo (N={N}) ---")
print(f"Consulta: P(L='T' | PM='T') ≈ {prob_rechazo:.5f}")
# (Debería ser similar al resultado de la enumeración, aprox 0.7)
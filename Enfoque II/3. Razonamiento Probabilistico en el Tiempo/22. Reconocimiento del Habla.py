# Algoritmo 22. Reconocimiento del Habla
# Alan Dorantes Verdin

import numpy as np

print("\n--- 22. Reconocimiento del Habla ---")

# --- 1. Definir los Modelos HMM ---
# (Usamos el algoritmo 'forward_pass' definido en el subtema 17)

# Observaciones: Simplificamos los fonemas a 'S1', 'S2', 'S3'
# 0='S1', 1='S2', 2='S3'

# --- Modelo 1: HMM para la palabra "HOLA" (2 estados: H-O)
pi_hola = np.array([1.0, 0.0]) # Siempre empieza en H
#       H     O
# H  [ 0.1,  0.9 ] # De H pasa a O
# O  [ 0.0,  1.0 ] # Se queda en O (bucle)
A_hola = np.array([
    [0.1, 0.9],
    [0.0, 1.0] 
])
#       S1    S2    S3
# H  [ 0.8,  0.1,  0.1 ] # H emite S1
# O  [ 0.1,  0.8,  0.1 ] # O emite S2
B_hola = np.array([
    [0.8, 0.1, 0.1],
    [0.1, 0.8, 0.1]
])
hmm_hola = {'pi': pi_hola, 'A': A_hola, 'B': B_hola, 'estados': [0, 1]}


# --- Modelo 2: HMM para la palabra "DIA" (2 estados: D-IA)
pi_dia = np.array([1.0, 0.0]) # Siempre empieza en D
#        D     IA
# D  [ 0.1,  0.9 ]
# IA [ 0.0,  1.0 ]
A_dia = np.array([
    [0.1, 0.9],
    [0.0, 1.0]
])
#       S1    S2    S3
# D  [ 0.1,  0.1,  0.8 ] # D emite S3
# IA [ 0.8,  0.1,  0.1 ] # IA emite S1
B_dia = np.array([
    [0.1, 0.1, 0.8],
    [0.8, 0.1, 0.1]
])
hmm_dia = {'pi': pi_dia, 'A': A_dia, 'B': B_dia, 'estados': [0, 1]}


# --- 2. Algoritmo Forward (Scoring) ---
def calcular_prob_forward(obs_seq, hmm):
    """
    Calcula la probabilidad P(obs_seq | hmm) usando el algoritmo Forward.
    """
    pi, A, B, estados = hmm['pi'], hmm['A'], hmm['B'], hmm['estados']
    
    alfa = np.zeros((len(obs_seq), len(estados)))
    
    # t = 0
    alfa[0, :] = pi * B[:, obs_seq[0]]
    
    # t = 1 a T-1
    for t in range(1, len(obs_seq)):
        for j in estados:
            alfa[t, j] = np.dot(alfa[t-1, :], A[:, j]) * B[j, obs_seq[t]]
            
    # La probabilidad total de la secuencia es la suma del último alfa
    prob_total = np.sum(alfa[-1, :])
    return prob_total


# --- 3. El Algoritmo de Reconocimiento ---
def reconocer_palabra(obs_seq, modelos):
    """
    Compara P(obs | modelo) para cada modelo y elige el mejor.
    """
    mejor_palabra = None
    mejor_prob = -1.0
    
    # 'modelos' es un diccionario: {'nombre': hmm_objeto}
    for nombre_palabra, hmm in modelos.items():
        
        prob = calcular_prob_forward(obs_seq, hmm)
        
        print(f"  P({obs_seq} | HMM_{nombre_palabra}) = {prob:.2e}")
        
        if prob > mejor_prob:
            mejor_prob = prob
            mejor_palabra = nombre_palabra
            
    return mejor_palabra, mejor_prob

# --- EJECUCIÓN ---
modelos_palabras = {
    "HOLA": hmm_hola,
    "DIA": hmm_dia
}

# Prueba 1: Una secuencia que se parece a "HOLA" (S1, S2, S2)
# (H emite S1, O emite S2)
obs1 = [0, 1, 1] 
print(f"Reconociendo secuencia {obs1} (S1, S2, S2)...")
palabra1, _ = reconocer_palabra(obs1, modelos_palabras)
print(f"==> Palabra reconocida: {palabra1}\n")

# Prueba 2: Una secuencia que se parece a "DIA" (S3, S1)
# (D emite S3, IA emite S1)
obs2 = [2, 0] 
print(f"Reconociendo secuencia {obs2} (S3, S1)...")
palabra2, _ = reconocer_palabra(obs2, modelos_palabras)
print(f"==> Palabra reconocida: {palabra2}")
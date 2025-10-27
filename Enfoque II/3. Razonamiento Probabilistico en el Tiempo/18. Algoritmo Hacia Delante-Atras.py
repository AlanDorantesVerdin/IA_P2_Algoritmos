# Algoritmo 18. Algoritmo Hacia Adelante-Atrás
# Alan Dorantes Verdin

print("\n--- 18. Algoritmo Hacia Adelante-Atrás ---")

# Definición de un HMM simple

# 1. Probabilidades Iniciales (pi)
# Empezamos con 60% Sol, 40% Lluvia
pi = {'Sol': 0.6, 'Lluvia': 0.4}

# 2. Matriz de Transición (A)
# (La misma que en el subtema 16)
transicion_A = {
    'Sol': {'Sol': 0.8, 'Lluvia': 0.2},
    'Lluvia': {'Sol': 0.4, 'Lluvia': 0.6}
}

# 3. Matriz de Emisión (B) - P(Observación | Estado Oculto)
# Observaciones: 'Paraguas', 'Helado'
emision_B = {
    # Dado que el estado es 'Sol'
    'Sol': {'Paraguas': 0.1, 'Helado': 0.9},
    # Dado que el estado es 'Lluvia'
    'Lluvia': {'Paraguas': 0.8, 'Helado': 0.2}
}

hmm_modelo = {
    'pi': pi,
    'A': transicion_A,
    'B': emision_B
}

# Usamos el 'hmm_modelo' y una secuencia de observaciones
hmm = hmm_modelo
observaciones = ['Paraguas', 'Helado', 'Paraguas']
estados = ['Sol', 'Lluvia']

def forward_pass(obs_seq):
    # alfa[t][estado] = P(estado_t, e_1:t)
    alfa = []
    
    # t = 0 (Inicialización)
    alfa_t0 = {}
    for e in estados:
        alfa_t0[e] = hmm['pi'][e] * hmm['B'][e][obs_seq[0]]
    alfa.append(alfa_t0)
    
    # t = 1 hasta T
    for t in range(1, len(obs_seq)):
        alfa_t = {}
        obs = obs_seq[t]
        
        for e_actual in estados:
            suma = 0
            for e_anterior in estados:
                # Suma( P(e_actual | e_anterior) * alfa[t-1][e_anterior] )
                suma += hmm['A'][e_anterior][e_actual] * alfa[t-1][e_anterior]
            
            # P(obs | e_actual) * Suma(...)
            alfa_t[e_actual] = hmm['B'][e_actual][obs] * suma
        alfa.append(alfa_t)
    
    return alfa

def backward_pass(obs_seq):
    # beta[t][estado] = P(e_t+1:T | estado_t)
    beta = [{} for _ in range(len(obs_seq))]
    
    # t = T-1 (Final)
    for e in estados:
        beta[-1][e] = 1.0 # Probabilidad base es 1
    
    # t = T-2 hasta 0
    for t in range(len(obs_seq) - 2, -1, -1):
        obs_siguiente = obs_seq[t+1]
        
        for e_actual in estados:
            suma = 0
            for e_siguiente in estados:
                suma += hmm['A'][e_actual][e_siguiente] * \
                        hmm['B'][e_siguiente][obs_siguiente] * \
                        beta[t+1][e_siguiente]
            beta[t][e_actual] = suma
            
    return beta

# --- Ejecución ---
obs = ['Paraguas', 'Helado']
alfa = forward_pass(obs)
beta = backward_pass(obs)

# Probabilidad de la secuencia (normalizador)
P_evidencia = sum(alfa[-1].values())

print(f"Observaciones: {obs}")
print(f"Prob. total de ver {obs}: {P_evidencia:.4f}")

# Calcular P(X_0 | 'Paraguas', 'Helado') (Suavizado en t=0)
prob_X0 = {}
for e in estados:
    prob_X0[e] = (alfa[0][e] * beta[0][e]) / P_evidencia

print(f"Prob. de Suavizado P(X_0 | {obs}):")
print(f"Sol: {prob_X0['Sol']:.4f}, Lluvia: {prob_X0['Lluvia']:.4f}")
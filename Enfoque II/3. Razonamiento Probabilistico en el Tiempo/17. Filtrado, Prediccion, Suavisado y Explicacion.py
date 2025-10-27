# Algoritmo 17. Filtrado, Predicción, Suavizado y Explicación
# Alan Dorantes Verdin

print("\n--- 17. Filtrado, Predicción, Suavizado y Explicación ---")

import numpy as np # Necesario para normalizar

# --- Modelo HMM (Requerido para los algoritmos) ---
# Estados Ocultos: 0 = 'Sol', 1 = 'Lluvia'
# Observaciones: 0 = 'Paraguas', 1 = 'Helado'
estados = [0, 1]
obs_map = {'Paraguas': 0, 'Helado': 1}

# P(X_0) - Probabilidades Iniciales
pi = np.array([0.6, 0.4])

# P(Xt | Xt-1) - Matriz de Transición (A)
#        Sol(t) Lluvia(t)
# Sol(t-1) [0.8,    0.2]
# Lluvia(t-1) [0.4,    0.6]
A = np.array([
    [0.8, 0.2],
    [0.4, 0.6]
])

# P(Et | Xt) - Matriz de Emisión (B)
#        Paraguas  Helado
# Sol    [ 0.1,     0.9 ]
# Lluvia [ 0.8,     0.2 ]
B = np.array([
    [0.1, 0.9],
    [0.8, 0.2]
])
# --- Fin del Modelo HMM ---

# --- Funciones de ayuda (Algoritmo Forward-Backward de 18) ---
# Necesitamos estas funciones para resolver las tareas de 17.

def forward_pass(obs_seq):
    """Calcula P(Xt, e_1:t) para todo t."""
    alfa = np.zeros((len(obs_seq), len(estados)))
    
    # t = 0
    alfa[0, :] = pi * B[:, obs_seq[0]]
    
    # t = 1 a T-1
    for t in range(1, len(obs_seq)):
        for j in estados: # Para cada estado actual j
            alfa[t, j] = np.dot(alfa[t-1, :], A[:, j]) * B[j, obs_seq[t]]
            
    return alfa

def backward_pass(obs_seq):
    """Calcula P(e_t+1:T | Xt) para todo t."""
    beta = np.zeros((len(obs_seq), len(estados)))
    
    # t = T-1 (último)
    beta[-1, :] = 1.0
    
    # t = T-2 a 0
    for t in range(len(obs_seq) - 2, -1, -1):
        for i in estados: # Para cada estado actual i
            beta[t, i] = np.dot(A[i, :], B[:, obs_seq[t+1]] * beta[t+1, :])
            
    return beta

# --- 1. ALGORITMO DE FILTRADO ---
def filtrado(obs_seq):
    """
    Tarea: Calcular P(Xt | e_1:t)
    (Prob. del estado actual, dada la evidencia hasta ahora)
    """
    # 1. Ejecutar el algoritmo 'Forward'
    alfa = forward_pass(obs_seq)
    
    # 2. La distribución en el último tiempo (t=T) es alfa[T-1]
    # 3. Normalizamos para obtener la probabilidad
    prob_filtrada = alfa[-1, :] / np.sum(alfa[-1, :])
    return prob_filtrada

# --- 2. ALGORITMO DE PREDICCIÓN ---
def prediccion(obs_seq, k_pasos):
    """
    Tarea: Calcular P(X_{t+k} | e_1:t)
    (Prob. de un estado futuro k pasos adelante)
    """
    # 1. Obtener la creencia actual (filtrado)
    creencia_actual = filtrado(obs_seq)
    
    # 2. Propagar la creencia k pasos hacia el futuro
    # Esto se hace multiplicando por la matriz de transición k veces
    creencia_futura = creencia_actual
    for _ in range(k_pasos):
        creencia_futura = np.dot(creencia_futura, A)
        
    return creencia_futura

# --- 3. ALGORITMO DE SUAVIZADO ---
def suavizado(obs_seq):
    """
    Tarea: Calcular P(Xk | e_1:T) para todo k < T
    (Prob. de un estado pasado, dada *toda* la evidencia)
    """
    alfa = forward_pass(obs_seq)
    beta = backward_pass(obs_seq)
    
    # P(Xk | e_1:T) = normalizado( alfa[k] * beta[k] )
    prob_suavizada = (alfa * beta) / np.sum(alfa * beta, axis=1, keepdims=True)
    return prob_suavizada

# --- 4. ALGORITMO DE EXPLICACIÓN (Algoritmo de Viterbi) ---
def explicacion_mas_probable(obs_seq):
    """
    Tarea: Encontrar la secuencia de estados x_1:T más probable.
    (Se usa el algoritmo de Viterbi)
    """
    T = len(obs_seq)
    N = len(estados)
    
    # T1[t, j] almacena la probabilidad de la ruta más probable hasta (t, j)
    T1 = np.zeros((T, N))
    # T2[t, j] almacena el estado anterior (en t-1) de esa ruta
    T2 = np.zeros((T, N), dtype=int)
    
    # t = 0
    T1[0, :] = pi * B[:, obs_seq[0]]
    
    # t = 1 a T-1
    for t in range(1, T):
        for j in estados:
            probs = T1[t-1, :] * A[:, j]
            T2[t, j] = np.argmax(probs)
            T1[t, j] = np.max(probs) * B[j, obs_seq[t]]
            
    # Recuperar la secuencia (Backtracking)
    secuencia_optima = np.zeros(T, dtype=int)
    secuencia_optima[-1] = np.argmax(T1[-1, :])
    
    for t in range(T - 2, -1, -1):
        secuencia_optima[t] = T2[t + 1, secuencia_optima[t + 1]]
        
    return secuencia_optima

# --- EJECUCIÓN ---
# Observaciones: Vimos 'Paraguas' (0), luego 'Helado' (1), luego 'Paraguas' (0)
evidencia = [0, 1, 0] 
print(f"Evidencia: ['Paraguas', 'Helado', 'Paraguas']\n")

# 1. Filtrado
prob_filtrada = filtrado(evidencia)
print(f"1. FILTRADO: P(X_2 | e_0:2)")
print(f"   P(Sol en t=2)={prob_filtrada[0]:.4f}, P(Lluvia en t=2)={prob_filtrada[1]:.4f}\n")

# 2. Predicción
prob_predicha = prediccion(evidencia, k_pasos=1)
print(f"2. PREDICCIÓN: P(X_3 | e_0:2)")
print(f"   P(Sol en t=3)={prob_predicha[0]:.4f}, P(Lluvia en t=3)={prob_predicha[1]:.4f}\n")

# 3. Suavizado
prob_suavizada = suavizado(evidencia)
print(f"3. SUAVIZADO: P(Xk | e_0:2)")
print(f"   t=0 (P(X_0 | ...)): Sol={prob_suavizada[0,0]:.4f}, Lluvia={prob_suavizada[0,1]:.4f}")
print(f"   t=1 (P(X_1 | ...)): Sol={prob_suavizada[1,0]:.4f}, Lluvia={prob_suavizada[1,1]:.4f}")
print(f"   t=2 (P(X_2 | ...)): Sol={prob_suavizada[2,0]:.4f}, Lluvia={prob_suavizada[2,1]:.4f}\n")

# 4. Explicación
secuencia = explicacion_mas_probable(evidencia)
map_estado = {0: 'Sol', 1: 'Lluvia'}
secuencia_nombres = [map_estado[s] for s in secuencia]
print(f"4. EXPLICACIÓN (Viterbi):")
print(f"   Secuencia más probable: {' -> '.join(secuencia_nombres)}")
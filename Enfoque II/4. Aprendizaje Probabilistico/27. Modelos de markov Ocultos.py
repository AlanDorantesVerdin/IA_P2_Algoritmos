# Algoritmo 27. Modelos de Markov Ocultos
# Alan Dorantes Verdin

import numpy as np

# --- 1. Funciones Prerrequisito (Forward y Backward) ---
# (Adaptadas de la implementación del subtema 17)

def forward_pass(obs_seq, pi, A, B):
    """Calcula P(Xt, e_1:t) para todo t."""
    N_estados = A.shape[0]
    T = len(obs_seq)
    alfa = np.zeros((T, N_estados))
    
    alfa[0, :] = pi * B[:, obs_seq[0]]
    
    for t in range(1, T):
        for j in range(N_estados):
            alfa[t, j] = np.dot(alfa[t-1, :], A[:, j]) * B[j, obs_seq[t]]
            
    return alfa

def backward_pass(obs_seq, A, B):
    """Calcula P(e_t+1:T | Xt) para todo t."""
    N_estados = A.shape[0]
    T = len(obs_seq)
    beta = np.zeros((T, N_estados))
    
    beta[T-1, :] = 1.0
    
    for t in range(T - 2, -1, -1):
        for i in range(N_estados):
            beta[t, i] = np.dot(A[i, :], B[:, obs_seq[t+1]] * beta[t+1, :])
            
    return beta

# --- 2. Algoritmo Baum-Welch (EM para HMMs) ---

def baum_welch(obs_seq, n_estados, n_obs, max_iter=20):
    """
    Aprende los parámetros A, B, pi de un HMM usando Baum-Welch.
    """
    T = len(obs_seq)
    
    # 1. Inicialización Aleatoria (con normalización)
    np.random.seed(42)
    pi = np.random.rand(n_estados)
    pi /= np.sum(pi)
    
    A = np.random.rand(n_estados, n_estados)
    A /= np.sum(A, axis=1, keepdims=True)
    
    B = np.random.rand(n_estados, n_obs)
    B /= np.sum(B, axis=1, keepdims=True)
    
    print("Iniciando Baum-Welch (Aprendizaje de HMM)...")

    for it in range(max_iter):
        
        # --- 2. PASO E (Expectation) ---
        # Calcular alfa y beta con los parámetros actuales
        alfa = forward_pass(obs_seq, pi, A, B)
        beta = backward_pass(obs_seq, A, B)
        
        # Probabilidad total de la secuencia (para normalizar)
        P_obs = np.sum(alfa[T-1, :])
        
        # gamma(i, t) = P(Estado_i en t | Obs, Params)
        gamma = (alfa * beta) / P_obs
        
        # xi(i, j, t) = P(Estado_i en t, Estado_j en t+1 | Obs, Params)
        xi = np.zeros((n_estados, n_estados, T - 1))
        for t in range(T - 1):
            for i in range(n_estados):
                xi[i, :, t] = (alfa[t, i] * A[i, :] * B[:, obs_seq[t+1]] * beta[t+1, :])
            # Normalizar xi en t
            xi[:, :, t] /= np.sum(xi[:, :, t])

        # --- 3. PASO M (Maximization) ---
        
        # Actualizar pi (prob. inicial)
        pi = gamma[0, :]
        
        # Actualizar A (transición)
        # A[i, j] = Suma_t(xi[i, j, t]) / Suma_t(gamma[i, t])
        suma_gamma_sin_final = np.sum(gamma[:-1, :], axis=0)
        suma_xi = np.sum(xi, axis=2)
        for i in range(n_estados):
            A[i, :] = suma_xi[i, :] / suma_gamma_sin_final[i]
        
        # Actualizar B (emisión)
        # B[j, k] = Suma_t(gamma[j, t] donde Obs_t == k) / Suma_t(gamma[j, t])
        suma_total_gamma = np.sum(gamma, axis=0)
        suma_gamma_obs = np.zeros((n_estados, n_obs))
        for t in range(T):
            k = obs_seq[t]
            suma_gamma_obs[:, k] += gamma[t, :]
            
        for j in range(n_estados):
            B[j, :] = suma_gamma_obs[j, :] / suma_total_gamma[j]
            
    print("Aprendizaje completado.")
    return pi, A, B

# --- Ejecución ---
# 0='Paraguas', 1='Helado'
# Estados ocultos (0='Sol', 1='Lluvia')
observaciones = [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1]
N_ESTADOS = 2
N_OBSERVACIONES = 2

pi_aprendido, A_aprendido, B_aprendido = baum_welch(
    observaciones, N_ESTADOS, N_OBSERVACIONES, max_iter=20
)

print("\n--- 27. Modelos de Markov Ocultos (Baum-Welch) ---")
print(f"\nPi (Inicial) aprendido:\n{pi_aprendido}")
print(f"\nA (Transición) aprendido:\n{A_aprendido}")
print(f"\nB (Emisión) aprendido:\n{B_aprendido}")
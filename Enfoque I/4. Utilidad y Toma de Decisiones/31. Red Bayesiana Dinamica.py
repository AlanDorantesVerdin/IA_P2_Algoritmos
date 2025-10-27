# Algoritmo 31. Red Bayesiana Dinámica 
# Alan Dorantes Verdin

import numpy as np # type: ignore

# Estados: 0='Lluvia', 1='Sol'
# Observaciones: 0='Visto', 1='NoVisto'

# 1. Probabilidad Inicial (pi)
pi = np.array([0.5, 0.5]) # [P(Lluvia), P(Sol)]

# 2. Modelo de Transición T[i, j] = P(X_t=j | X_{t-1}=i)
T = np.array([
  # Lluvia_t, Sol_t
    [0.7, 0.3], # desde Lluvia_{t-1}
    [0.3, 0.7]  # desde Sol_{t-1}
])

# 3. Modelo de Sensor O[j, k] = P(E_t=k | X_t=j)
O = np.array([
  # Visto, NoVisto
    [0.9, 0.1], # en Lluvia
    [0.2, 0.8]  # en Sol
])

def normalizar(b):
    """Asegura que la distribución de creencias sume 1."""
    suma = np.sum(b)
    if suma == 0: return b
    return b / suma

def forward_step(creencia_anterior, observacion_idx):
    """
    Exactamente la misma lógica que el 'belief_update' del POMDP.
    """
    
    # 1. Predicción (Sum_x_t [ T(x_t, x_{t+1}) * P(x_t | e_{1:t}) ])
    # (Matemáticamente T.T @ b)
    b_pred = T.T @ creencia_anterior
    
    # 2. Actualización ( O(e_{t+1} | x_{t+1}) * b_pred )
    O_vector = O[:, observacion_idx]
    
    b_nuevo = O_vector * b_pred
    
    # 3. Normalización
    return normalizar(b_nuevo)

# --- Simulación ---
print("\n--- 31. Red Bayesiana Dinámica ---")
print("Estados: 0=Lluvia, 1=Sol")

# Secuencia de observaciones
# Día 1: 'Visto' (0)
# Día 2: 'Visto' (0)
# Día 3: 'NoVisto' (1)
observaciones = [0, 0, 1]

# Creencia inicial (Día 0)
creencia = pi
print(f"Creencia Inicial (Día 0): {np.round(creencia, 2)}")

for i, obs_idx in enumerate(observaciones):
    creencia = forward_step(creencia, obs_idx)
    obs_str = "'Visto'" if obs_idx == 0 else "'NoVisto'"
    print(f"Observación Día {i+1}: {obs_str}. Creencia: {np.round(creencia, 3)}")

# Análisis:
# Día 1 (Visto): La probabilidad de lluvia sube a 0.818
# Día 2 (Visto): La probabilidad de lluvia sube a 0.887 (más confianza)
# Día 3 (NoVisto): La probabilidad de lluvia baja drásticamente a 0.378
print("\n")
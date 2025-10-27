# Algoritmo 30. MDP Parcialmente Observable (POMDP)
# Alan Dorantes Verdin

import numpy as np # type: ignore

# 1. Definición del POMDP
estados = [0, 1, 2]
accion = 'Mover'

# 2. Modelo de Transición T(s, a, s') -> T[s][s'] para la acción 'Mover'
# (La acción 'Mover' es 0->1, 1->2, 2->0)
T = np.array([
  # s'
  # 0  1  2  <- (desde s)
    [0, 1, 0], # 0
    [0, 0, 1], # 1
    [1, 0, 0]  # 2
])

# 3. Modelo de Observación O(o | s') -> O[s'][o]
# (Columna 0 = Obs 'A', Columna 1 = Obs 'B')
O = np.array([
  # 'A' 'B'
    [0.9, 0.1], # s'=0
    [0.0, 1.0], # s'=1
    [0.9, 0.1]  # s'=2
])

def normalizar(b):
    """Asegura que la distribución de creencias sume 1."""
    suma = np.sum(b)
    if suma == 0: return b
    return b / suma

def belief_update(b, observacion_idx):
    """
    Actualiza la creencia 'b' usando la acción 'Mover' y la 'observacion_idx'.
    'b' es un vector [P(s=0), P(s=1), P(s=2)]
    'observacion_idx' es 0 para 'A', 1 para 'B'.
    """
    
    # 1. Predicción (Prediction Step)
    # b_pred(s') = Sum_s [ T(s, 'Mover', s') * b(s) ]
    # (Esto es una multiplicación de matriz-vector)
    # T.T es la transpuesta de T, para alinearla con el vector 'b'
    b_pred = T.T @ b 
    
    # 2. Actualización (Update Step)
    # b'(s') = O(o | s') * b_pred(s')
    # (Esto es una multiplicación elemento a elemento)
    
    # Extraemos la columna de probabilidad para la observación recibida
    O_vector = O[:, observacion_idx] 
    
    b_nuevo = O_vector * b_pred
    
    # 3. Normalización (Eta)
    return normalizar(b_nuevo)

# --- Simulación ---
print("\n--- 30. MDP Parcialmente Observable (POMDP) ---")

# Creencia inicial: Estamos 100% seguros de estar en s=0
creencia = np.array([1.0, 0.0, 0.0])
print(f"Creencia Inicial b_0:    {creencia} (Seguros de estar en s=0)")

# --- Paso 1 ---
# Tomamos la acción 'Mover'. El estado real ahora es s=1.
# El agente recibe la Observación 'B' (que es 100% probable en s=1).
obs_idx = 1 # 'B'
creencia = belief_update(creencia, obs_idx)
print(f"Acción: 'Mover', Obs: 'B'. Creencia b_1: {np.round(creencia, 2)} (Seguros de estar en s=1)")

# --- Paso 2 ---
# Tomamos la acción 'Mover'. El estado real ahora es s=2.
# El agente recibe la Observación 'A' (que es 90% probable en s=2).
obs_idx = 0 # 'A'
creencia = belief_update(creencia, obs_idx)
print(f"Acción: 'Mover', Obs: 'A'. Creencia b_2: {np.round(creencia, 2)} (Seguros de estar en s=2)")

# --- Paso 3 ---
# Tomamos la acción 'Mover'. El estado real ahora es s=0.
# El agente recibe la Observación 'A' (que es 90% probable en s=0).
obs_idx = 0 # 'A'
creencia = belief_update(creencia, obs_idx)
print(f"Acción: 'Mover', Obs: 'A'. Creencia b_3: {np.round(creencia, 2)} (¡Incertidumbre!)")

# ¡AQUÍ ESTÁ LA INCERTIDUMBRE!
# Después de ver 'A', el agente no sabe si está en s=0 o s=2,
# porque la observación es idéntica para ambos.
print("\n")
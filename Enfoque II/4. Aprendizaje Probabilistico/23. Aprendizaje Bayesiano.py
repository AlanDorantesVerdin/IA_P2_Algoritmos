# Algoritmo 23. Aprendizaje Bayesiano
# Alan Dorantes Verdin

print("\n--- 23. Aprendizaje Bayesiano ---")

import numpy as np

def aprendizaje_bayesiano_moneda(lanzamientos, alfa_previo, beta_previo):
    """
    Actualiza la creencia sobre la probabilidad de 'cara' (theta) de una moneda.
    
    :param lanzamientos: Una lista de 0s (cruz) y 1s (cara).
    :param alfa_previo: El parámetro 'alfa' de nuestra creencia previa (Beta).
    :param beta_previo: El parámetro 'beta' de nuestra creencia previa (Beta).
    """
    
    print(f"Creencia Previa: Beta(alfa={alfa_previo}, beta={beta_previo})")
    
    # Estimación previa de P(Cara) = alfa / (alfa + beta)
    estimacion_previa = alfa_previo / (alfa_previo + beta_previo)
    print(f"Estimación previa de P(Cara): {estimacion_previa:.4f}")
    
    # 1. Contar la evidencia
    N = len(lanzamientos)
    H = sum(lanzamientos) # Número de Caras (1s)
    T = N - H             # Número de Cruces (0s)
    
    print(f"\nEvidencia: {N} lanzamientos, {H} caras, {T} cruces.")
    
    # 2. Actualizar los parámetros
    alfa_posterior = alfa_previo + H
    beta_posterior = beta_previo + T
    
    print(f"\nCreencia Posterior: Beta(alfa={alfa_posterior}, beta={beta_posterior})")

    # Estimación posterior de P(Cara)
    estimacion_posterior = alfa_posterior / (alfa_posterior + beta_posterior)
    print(f"Estimación posterior de P(Cara): {estimacion_posterior:.4f}")

# --- Ejecución ---
# Empezamos con una creencia "plana" o "ignorante": Beta(1, 1)
# Esto significa que cualquier probabilidad P(Cara) entre 0 y 1 es igualmente probable.
alfa_inicial = 1
beta_inicial = 1

# Vemos 10 lanzamientos: [1, 0, 1, 1, 0, 1, 0, 1, 1, 0] (6 caras, 4 cruces)
evidencia = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0]

aprendizaje_bayesiano_moneda(evidencia, alfa_inicial, beta_inicial)
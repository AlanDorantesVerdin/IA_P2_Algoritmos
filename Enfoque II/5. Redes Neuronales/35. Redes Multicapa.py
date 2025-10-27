# Algoritmo 35. Redes Multicapa
# Alan Dorantes Verdin

import numpy as np
# (Usamos la función sigmoid de el Algoritmo 32)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def forward_pass_multicapa(X, pesos_oculta, sesgo_oculta, pesos_salida, sesgo_salida):
    """
    Calcula la predicción de una red de 1 capa oculta.
    """
    
    # 1. Capa de Entrada -> Capa Oculta
    # z_oculta = X * W_oculta + b_oculta
    z_oculta = np.dot(X, pesos_oculta) + sesgo_oculta
    # a_oculta = f(z_oculta)
    a_oculta = sigmoid(z_oculta)
    
    # 2. Capa Oculta -> Capa de Salida
    # z_salida = a_oculta * W_salida + b_salida
    z_salida = np.dot(a_oculta, pesos_salida) + sesgo_salida
    # a_salida = f(z_salida)
    prediccion = sigmoid(z_salida)
    
    return prediccion

# --- Ejecución ---
# (Pesos y sesgos aleatorios solo para demostración)
np.random.seed(42)
X_test = np.array([1, 0]) # Entrada (1x2)

# Pesos Oculta (2x3) -> 3 neuronas ocultas
W_h = np.random.rand(2, 3) 
b_h = np.random.rand(1, 3)
# Pesos Salida (3x1) -> 1 neurona de salida
W_o = np.random.rand(3, 1)
b_o = np.random.rand(1, 1)

print("\n--- 35. Redes Multicapa (Forward Pass) ---")
pred = forward_pass_multicapa(X_test, W_h, b_h, W_o, b_o)
print(f"Entrada: {X_test}")
print(f"Predicción de la Red: {pred[0][0]:.4f}")
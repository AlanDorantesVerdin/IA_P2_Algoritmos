# Algoritmo 32. Funciones de Activación
# Alan Dorantes Verdin

import numpy as np

# --- 1. Sigmoid ---
# Rango: (0, 1). Usada en capas de salida para probabilidad.
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def derivada_sigmoid(z):
    s = sigmoid(z)
    return s * (1 - s)

# --- 2. Tanh (Tangente Hiperbólica) ---
# Rango: (-1, 1). Versión "centrada en cero" de Sigmoid.
def tanh(z):
    return np.tanh(z)

def derivada_tanh(z):
    t = tanh(z)
    return 1 - (t**2)

# --- 3. ReLU (Rectified Linear Unit) ---
# Rango: [0, inf). La más popular en capas ocultas. Muy rápida.
def relu(z):
    # Devuelve 0 si z < 0, o z si z >= 0
    return np.maximum(0, z)

def derivada_relu(z):
    # Devuelve 1 si z > 0, 0 si z <= 0
    return (z > 0).astype(float)

# --- Ejecución ---
z_test = np.array([-2, -5, 1, 5, 2])
print("\n--- 32. Funciones de Activación ---")
print(f"Valores de Z: {z_test}")
print(f"Sigmoid(Z): {np.round(sigmoid(z_test), 2)}")
print(f"Tanh(Z): {np.round(tanh(z_test), 2)}")
print(f"ReLU(Z): {np.round(relu(z_test), 2)}")
print(f"Derivada de ReLU(Z): {np.round(derivada_relu(z_test), 2)}")
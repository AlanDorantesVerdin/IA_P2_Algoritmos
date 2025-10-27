# Algoritmo 31. Computación Neuronal
# Alan Dorantes Verdin

import numpy as np

def funcion_activacion_ejemplo(z):
    """Una función de activación simple (Sigmoid)."""
    return 1 / (1 + np.exp(-z))

def computo_neuronal(entradas, pesos, sesgo):
    """
    Calcula la salida de una única neurona.
    
    :param entradas: vector (array) de entradas [x1, x2, ...]
    :param pesos: vector (array) de pesos [w1, w2, ...]
    :param sesgo: un solo valor (b)
    """
    
    # 1. Calcular la suma ponderada (Producto punto)
    # z = (w1*x1 + w2*x2 + ...)
    z = np.dot(entradas, pesos)
    
    # 2. Añadir el sesgo
    z = z + sesgo
    
    # 3. Aplicar la función de activación
    y = funcion_activacion_ejemplo(z)
    
    return y

# --- Ejecución ---
# Una neurona con 3 entradas
x = np.array([0.5, 1.0, -0.2]) # Entradas
w = np.array([0.8, -0.4, 0.1]) # Pesos
b = 0.1                        # Sesgo

salida_neurona = computo_neuronal(x, w, b)

print("\n--- 31. Computación Neuronal ---")
print(f"Entradas (x): {x}")
print(f"Pesos (w):    {w}")
print(f"Sesgo (b):    {b}")
print(f"Salida (y):   {salida_neurona:.4f}")
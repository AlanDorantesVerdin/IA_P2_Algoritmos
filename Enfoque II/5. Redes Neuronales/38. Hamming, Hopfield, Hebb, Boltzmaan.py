# Algoritmo 38. Hamming, Hopfield, Hebb, Boltzmann
# Alan Dorantes Verdin

import numpy as np

def regla_de_hebb(X, n_neuronas):
    """
    Calcula la matriz de pesos usando la regla de Hebb simple.
    (Asume que X son patrones bipolares {-1, 1})
    """
    n_features = X.shape[1]
    W = np.zeros((n_features, n_features))
    
    # Por cada patrón
    for p in X:
        # W = W + (p^T * p)
        W += np.outer(p, p)
        
    # Poner la diagonal a cero (las neuronas no se conectan a sí mismas)
    np.fill_diagonal(W, 0)
    
    return W

# --- Ejecución Hebb (para Red de Hopfield) ---
# Patrones bipolares {-1, 1} a memorizar
# (Simplificamos a 1D para que np.outer funcione)
patron1 = np.array([1, -1, 1, -1])
patron2 = np.array([1, 1, -1, -1])
X_hopfield = np.array([patron1, patron2])

W_hebb = regla_de_hebb(X_hopfield, 4)
print("\n--- 38. Regla de Hebb ---")
print(f"Matriz de pesos (W) aprendida con Hebb:\n{W_hebb}")


def hopfield_recuperar(patron_ruidoso, W, max_iter=20):
    """
    Recupera un patrón de una red de Hopfield.
    """
    s = np.copy(patron_ruidoso)
    n_neuronas = len(s)
    
    for _ in range(max_iter):
        estado_cambio = False
        
        # Actualización asíncrona (neurona por neurona)
        for i in range(n_neuronas):
            # Calcular suma ponderada
            z = np.dot(W[i, :], s)
            
            # Aplicar función signo
            s_nuevo_i = 1 if z >= 0 else -1
            
            if s[i] != s_nuevo_i:
                s[i] = s_nuevo_i
                estado_cambio = True
        
        # Si no hubo cambios, convergió
        if not estado_cambio:
            break
            
    return s

# --- Ejecución Hopfield ---
# (Usamos W_hebb aprendida arriba)
# W_hebb memoriza [1, -1, 1, -1] y [1, 1, -1, -1]

# Patrón ruidoso (similar al patron1)
p_ruido = np.array([1, -1, -1, -1]) 

print("\n--- 38. Red de Hopfield ---")
print(f"Matriz de pesos (W):\n{W_hebb}")
print(f"Patrón ruidoso:  {p_ruido}")

p_recuperado = hopfield_recuperar(p_ruido, W_hebb)
print(f"Patrón recuperado: {p_recuperado}")
print(f"Patrón original 1: {patron1}")

# Red Hamming consiste en medir la distancia Hamming entre patrones
# y clasificar según la mínima distancia.
# Red Boltzmann consiste en una red estocástica que minimiza energía.
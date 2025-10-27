# Algoritmo 36. Retropropagación del Error
# Alan Dorantes Verdin

import numpy as np
# (Usamos sigmoid y derivada_sigmoid de el Algoritmo 32)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def derivada_sigmoid(z):
    s = sigmoid(z)
    return s * (1 - s)

def backward_pass(X, y_real, W_h, W_o, z_h, a_h, z_o, a_o, tasa_aprendizaje):
    """
    Implementación simple de un paso de Backpropagation.
    (Las 'z' y 'a' vienen del forward pass).
    """
    
    # 1. Calcular el Error y Gradiente en la Capa de Salida
    # (Usamos error cuadrático medio)
    error_salida = y_real - a_o
    d_cost_d_z_salida = error_salida * derivada_sigmoid(z_o)
    
    # 2. Calcular el Error y Gradiente en la Capa Oculta
    # Propagar el error hacia atrás
    error_oculta = np.dot(d_cost_d_z_salida, W_o.T)
    d_cost_d_z_oculta = error_oculta * derivada_sigmoid(z_h)
    
    # 3. Calcular Gradientes de los Pesos (d_cost / d_W)
    # Gradiente Pesos Salida (W_o)
    grad_W_o = np.dot(a_h.T, d_cost_d_z_salida)
    # Gradiente Pesos Oculta (W_h)
    grad_W_h = np.dot(X.T, d_cost_d_z_oculta)
    
    # 4. Actualizar Pesos (Descenso de Gradiente)
    W_o_nuevo = W_o + (grad_W_o * tasa_aprendizaje)
    W_h_nuevo = W_h + (grad_W_h * tasa_aprendizaje)
    
    return W_h_nuevo, W_o_nuevo

# --- Ejecución (Conceptual) ---
# (Simulamos los valores de un forward pass para ejecutar el backward pass)
print("\n--- 36. Retropropagación del Error ---")
# Simulación: 1 muestra de (2 features) -> 3 ocultas -> 1 salida
X = np.array([[1, 0]]) # (1x2)
y = np.array([[1]])    # (1x1)
W_h = np.random.rand(2, 3) # (2x3)
W_o = np.random.rand(3, 1) # (3x1)
z_h = np.random.rand(1, 3); a_h = sigmoid(z_h) # (1x3)
z_o = np.random.rand(1, 1); a_o = sigmoid(z_o) # (1x1)

print(f"Pesos Oculta (Antes): \n{W_h}")
W_h_act, W_o_act = backward_pass(X, y, W_h, W_o, z_h, a_h, z_o, a_o, 0.1)
print(f"Pesos Oculta (Después): \n{W_h_act}")
print("Los pesos cambiaron según el error.")
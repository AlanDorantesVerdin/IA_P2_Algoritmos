# Algoritmo 34. Separabilidad Lineal
# Alan Dorantes Verdin

import numpy as np
# (Usamos perceptron_entrenar y X_and/y_and de arriba)

def funcion_escalon(z):
    """Función de activación del Perceptrón."""
    return (z >= 0).astype(int) # 1 si z >= 0, 0 si z < 0

def perceptron_entrenar(X, y, epochs, tasa_aprendizaje):
    """
    Entrena un Perceptrón simple.
    """
    n_muestras, n_features = X.shape
    # Inicializar pesos y sesgo a cero
    w = np.zeros(n_features)
    b = 0.0
    
    for epoch in range(epochs):
        errores_totales = 0
        for i in range(n_muestras):
            x_i = X[i]
            y_real = y[i]
            
            # 1. Calcular suma ponderada (z)
            z = np.dot(x_i, w) + b
            # 2. Calcular predicción (y_pred)
            y_pred = funcion_escalon(z)
            
            # 3. Calcular error
            error = y_real - y_pred
            
            # 4. Actualizar pesos (si hay error)
            if error != 0:
                errores_totales += 1
                delta_w = tasa_aprendizaje * error * x_i
                delta_b = tasa_aprendizaje * error
                
                w += delta_w
                b += delta_b
                
        # Si no hubo errores, hemos convergido
        if errores_totales == 0:
            print(f"Convergencia alcanzada en epoch {epoch+1}")
            break
            
    return w, b

# X: [0,0], [0,1], [1,0], [1,1]
X_and = np.array([[0,0], [0,1], [1,0], [1,1]])
# y: 0, 0, 0, 1
y_and = np.array([0, 0, 0, 1])

# --- 1. Problema Linealmente Separable (AND) ---
print("\n--- 34. Separabilidad Lineal (Prueba 1: AND) ---")
# Esto ya lo ejecutamos en el subtema 33.
# El Perceptrón SÍ convergió.
print("El Perceptrón CONVERGIÓ para AND (es linealmente separable).")


# --- 2. Problema No Linealmente Separable (XOR) ---
# X: [0,0], [0,1], [1,0], [1,1]
X_xor = np.array([[0,0], [0,1], [1,0], [1,1]])
# y: 0, 1, 1, 0
y_xor = np.array([0, 1, 1, 0])

print("\n--- 34. Separabilidad Lineal (Prueba 2: XOR) ---")
# Entrenamos por 100 epochs. Si no converge, falla.
w_xor, b_xor = perceptron_entrenar(X_xor, y_xor, epochs=100, tasa_aprendizaje=0.1)

# Probar
print("Resultados del Perceptrón en XOR (falla):")
for x_i in X_xor:
    pred = funcion_escalon(np.dot(x_i, w_xor) + b_xor)
    print(f"Entrada: {x_i} -> Predicción: {pred}")

print("El Perceptrón NO convergió (no es linealmente separable).")
# Algoritmo 33. Perceptron, ADALINE y MADALINE
# Alan Dorantes Verdin

import numpy as np

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

# --- Ejecución (Problema AND) ---
# X: [0,0], [0,1], [1,0], [1,1]
X_and = np.array([[0,0], [0,1], [1,0], [1,1]])
# y: 0, 0, 0, 1
y_and = np.array([0, 0, 0, 1])

print("\n--- 33. Perceptrón (para AND) ---")
w_p, b_p = perceptron_entrenar(X_and, y_and, epochs=100, tasa_aprendizaje=0.1)
print(f"Pesos finales: {w_p}, Sesgo final: {b_p}")

# Probar
for x_i in X_and:
    pred = funcion_escalon(np.dot(x_i, w_p) + b_p)
    print(f"Entrada: {x_i} -> Predicción: {pred}")


# (funcion_escalon definida arriba)

def adaline_entrenar(X, y, epochs, tasa_aprendizaje):
    """
    Entrena un ADALINE usando la Regla Delta.
    """
    n_muestras, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0
    
    for epoch in range(epochs):
        for i in range(n_muestras):
            x_i = X[i]
            y_real = y[i] # y_real debe ser {+1, -1} para ADALINE
            
            # 1. Calcular suma ponderada (z)
            z = np.dot(x_i, w) + b
            
            # 2. Calcular error (antes de la activación)
            error = y_real - z
            
            # 3. Actualizar pesos (Regla Delta)
            delta_w = tasa_aprendizaje * error * x_i
            delta_b = tasa_aprendizaje * error
            
            w += delta_w
            b += delta_b
            
    return w, b

# --- Ejecución (Problema OR) ---
# Usamos {+1, -1} para las etiquetas de ADALINE
# X: [0,0], [0,1], [1,0], [1,1]
X_or = np.array([[0,0], [0,1], [1,0], [1,1]])
# y: -1, 1, 1, 1
y_or_adal = np.array([-1, 1, 1, 1])

print("\n--- 33. ADALINE (para OR) ---")
w_a, b_a = adaline_entrenar(X_or, y_or_adal, epochs=100, tasa_aprendizaje=0.1)
print(f"Pesos finales: {w_a}, Sesgo final: {b_a}")

# Probar (Usamos 1 si z >= 0, -1 si z < 0)
for x_i in X_or:
    z = np.dot(x_i, w_a) + b_a
    pred = 1 if z >= 0 else -1
    print(f"Entrada: {x_i} -> Predicción: {pred}")

# MEADELINE es una red de múltiples neuronas ADALINE, usualmente en una capa oculta, 
# que alimenta una neurona de salida. El "algoritmo" es la estructura de la red.
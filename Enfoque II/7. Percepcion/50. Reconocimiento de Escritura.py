# Algoritmo 50. Reconocimiento de Escritura
# Alan Dorantes Verdin

import numpy as np

# (Usamos la función 'distancia_euclidiana' de antes, si fuera necesaria)
# (Usaremos la implementación de k-NN del Subtema 28)
def k_vecinos_cercanos(X_ent, y_ent, x_nuevo, k=3):
    distancias = []
    for i in range(len(X_ent)):
        dist = np.sqrt(np.sum((X_ent[i] - x_nuevo)**2)) # Euclidiana
        distancias.append((dist, y_ent[i]))
    distancias.sort(key=lambda item: item[0])
    k_vecinos = distancias[:k]
    clases_vecinos = [vecino[1] for vecino in k_vecinos]
    conteo_votos = {}
    for clase in clases_vecinos:
        conteo_votos[clase] = conteo_votos.get(clase, 0) + 1
    return max(conteo_votos, key=conteo_votos.get)

# --- Algoritmo de Reconocimiento ---
def extraer_features_simples(img_digito):
    """
    Extrae un vector de 2 features: suma de la mitad superior e inferior.
    """
    alto = img_digito.shape[0]
    mitad = alto // 2
    
    feature_superior = np.sum(img_digito[0:mitad, :])
    feature_inferior = np.sum(img_digito[mitad:, :])
    
    return np.array([feature_superior, feature_inferior])

# --- Ejecución ---
print("\n--- 50. Reconocimiento de Escritura (k-NN) ---")

# 1. Datos de "entrenamiento" (dígitos 5x5)
# (1 = pixel encendido, 0 = apagado)
digito_1 = np.array([
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0]
])

digito_7 = np.array([
    [1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
])

digito_0 = np.array([
    [1, 1, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 0, 0]
])

# 2. Extraer features de entrenamiento
X_entrenamiento = np.array([
    extraer_features_simples(digito_1),
    extraer_features_simples(digito_7),
    extraer_features_simples(digito_0)
])
y_entrenamiento = np.array([1, 7, 0]) # Etiquetas

print(f"Features (Sup, Inf): {X_entrenamiento.T}")
print(f"Etiquetas: {y_entrenamiento}")

# 3. Dígito "desconocido" (un '1' ruidoso)
digito_nuevo = np.array([
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0]
])
features_nuevo = extraer_features_simples(digito_nuevo)

# 4. Clasificar
prediccion = k_vecinos_cercanos(X_entrenamiento, y_entrenamiento, features_nuevo, k=1)
print(f"\nFeatures del dígito nuevo: {features_nuevo}")
print(f"Predicción de k-NN (k=1): {prediccion}")
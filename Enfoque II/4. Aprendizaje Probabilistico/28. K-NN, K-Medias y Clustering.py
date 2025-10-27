# Algoritmo 28. K-NN, K-Medias y Clustering
# Alan Dorantes Verdin

print("\n--- 28. K-NN, K-Medias y Clustering ---\n")

import numpy as np

def distancia_euclidiana(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.sqrt(np.sum((p1 - p2)**2))

def k_vecinos_cercanos(X_ent, y_ent, x_nuevo, k=3):
    """
    Clasificador k-NN simple.
    """
    distancias = []
    # 1. Calcular distancia a todos los puntos de entrenamiento
    for i in range(len(X_ent)):
        dist = distancia_euclidiana(X_ent[i], x_nuevo)
        distancias.append((dist, y_ent[i]))
        
    # 2. Ordenar por distancia y tomar los k primeros
    distancias.sort(key=lambda item: item[0])
    k_vecinos = distancias[:k]
    
    # 3. Votar por la clase
    clases_vecinos = [vecino[1] for vecino in k_vecinos]
    
    # Contar votos (encontrar la moda)
    # (Forma simple de encontrar el más común)
    conteo_votos = {}
    for clase in clases_vecinos:
        conteo_votos[clase] = conteo_votos.get(clase, 0) + 1
        
    # Encontrar la clase con más votos
    clase_ganadora = max(conteo_votos, key=conteo_votos.get)
    
    return clase_ganadora

# --- Ejecución k-NN ---
# (Datos de Naive Bayes)
X_ent_knn = np.array([[180, 85], [175, 75], [185, 90], [160, 55], [165, 60], [170, 65]])
y_ent_knn = np.array([0, 0, 0, 1, 1, 1]) # 0=Hombre, 1=Mujer

x_nuevo_knn = np.array([168, 60]) # Nuevo punto
k = 3

pred_knn = k_vecinos_cercanos(X_ent_knn, y_ent_knn, x_nuevo_knn, k=k)
print(f"--- k-NN (k-Vecinos más Cercanos) ---")
print(f"Punto nuevo: {x_nuevo_knn}")
print(f"Predicción (k={k}): {pred_knn} (1=Mujer)")

def k_medias(X, k=2, max_iter=100):
    """
    Algoritmo k-Means simple.
    """
    n_muestras, n_features = X.shape
    
    # 1. Inicializar centroides (eligiendo k puntos al azar)
    indices_azar = np.random.choice(n_muestras, k, replace=False)
    centroides = X[indices_azar]
    
    for _ in range(max_iter):
        # 2. Paso de Asignación
        etiquetas = np.zeros(n_muestras)
        for i in range(n_muestras):
            punto = X[i]
            # Calcular distancias a todos los centroides
            distancias = [distancia_euclidiana(punto, c) for c in centroides]
            # Asignar al más cercano
            etiquetas[i] = np.argmin(distancias)
            
        centroides_nuevos = np.zeros((k, n_features))
        
        # 3. Paso de Actualización
        for c in range(k):
            # Obtener todos los puntos asignados a este cluster
            puntos_cluster = X[etiquetas == c]
            if len(puntos_cluster) > 0:
                # Calcular la media (nuevo centroide)
                centroides_nuevos[c] = np.mean(puntos_cluster, axis=0)
                
        # 4. Verificar convergencia
        if np.all(centroides == centroides_nuevos):
            break
            
        centroides = centroides_nuevos
        
    return centroides, etiquetas

# --- Ejecución k-Means ---
# (Datos de Naive Bayes)
X_km = np.array([[180, 85], [175, 75], [185, 90], [160, 55], [165, 60], [170, 65]])
k = 2

print(f"\n--- k-Medias (k-Means) ---")
print(f"Ejecutando k-Means para k={k}...")
centroides_km, etiquetas_km = k_medias(X_km, k=k)

print(f"Centroides finales:\n {centroides_km}")
print(f"Etiquetas asignadas: {etiquetas_km}")
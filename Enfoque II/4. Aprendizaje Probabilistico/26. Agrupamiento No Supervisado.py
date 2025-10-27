# Algoritmo 26. Agrupamiento No Supervisado
# Alan Dorantes Verdin

import numpy as np

# --- 1. Funciones de Ayuda ---

def distancia_euclidiana(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.sqrt(np.sum((p1 - p2)**2))

def obtener_vecinos(X, punto_idx, eps):
    """
    Encuentra los índices de todos los puntos a una distancia 'eps'
    del punto en 'punto_idx'.
    """
    vecinos = []
    punto_central = X[punto_idx]
    for i in range(len(X)):
        if i == punto_idx:
            continue
        if distancia_euclidiana(punto_central, X[i]) <= eps:
            vecinos.append(i)
    return vecinos

# --- 2. Algoritmo DBSCAN ---

def dbscan(X, eps, min_pts):
    """
    Implementación simple de DBSCAN.
    """
    # Etiquetas: -1 = Sin visitar, 0 = Ruido, 1, 2, 3... = ID del Cluster
    n_muestras = len(X)
    etiquetas = np.full(n_muestras, -1) 
    
    cluster_id = 0
    
    # Iterar sobre cada punto
    for i in range(n_muestras):
        # Si ya visitamos este punto, continuar
        if etiquetas[i] != -1:
            continue
            
        # Encontrar vecinos
        vecinos_i = obtener_vecinos(X, i, eps)
        
        # Si no es un punto central, marcar como ruido (por ahora)
        if len(vecinos_i) < min_pts:
            etiquetas[i] = 0 # Marcar como ruido
            continue
            
        # ¡Es un punto central! Empezar un nuevo cluster
        cluster_id += 1
        etiquetas[i] = cluster_id
        
        # --- Expansión del Cluster ---
        # Procesar todos los vecinos de este punto central
        cola_expansion = list(vecinos_i)
        
        while cola_expansion:
            j = cola_expansion.pop(0) # Tomar el siguiente vecino
            
            # Si era ruido, ahora pertenece a este cluster
            if etiquetas[j] == 0:
                etiquetas[j] = cluster_id
                
            # Si ya fue visitado (en otro cluster o en este), continuar
            if etiquetas[j] != -1:
                continue
                
            # Marcar como parte del cluster actual
            etiquetas[j] = cluster_id
            
            # Encontrar *sus* vecinos
            vecinos_j = obtener_vecinos(X, j, eps)
            
            # Si este vecino *también* es un punto central...
            if len(vecinos_j) >= min_pts:
                # ...añadir a todos sus vecinos a la cola de expansión
                cola_expansion.extend(vecinos_j)
                
    return etiquetas

# --- Ejecución ---
# Datos: Dos "lunas" (clusters no circulares)
from sklearn.datasets import make_moons
X_db, y_real = make_moons(n_samples=200, noise=0.05, random_state=0)

# eps=0.3 y min_pts=5 son buenos parámetros para este dataset
etiquetas_db = dbscan(X_db, eps=0.3, min_pts=5)

print("\n--- 26. Agrupamiento No Supervisado (DBSCAN) ---")
print(f"Puntos de datos: {len(X_db)}")
print("Etiquetas asignadas (primeros 20):")
print(etiquetas_db[:20])
print(f"Clusters encontrados: {len(np.unique(etiquetas_db[etiquetas_db > 0]))}")
# (Nota: El resultado 0 es 'Ruido')
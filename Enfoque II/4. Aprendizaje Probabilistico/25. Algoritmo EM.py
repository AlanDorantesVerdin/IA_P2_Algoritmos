# Algoritmo 25. Algoritmo EM
# Alan Dorantes Verdin

print("\n--- 25. Algoritmo EM ---")

import numpy as np

# Implementación simple de EM para 1D GMM (Mezcla de 2 Gaussianas)
# Objetivo: Encontrar las medias (mu1, mu2) y varianzas (var1, var2)
# de dos grupos (clusters) en datos 1D.

def pdf_gaussiana(x, media, var):
    """Calcula la PDF Gaussiana (simplificada)."""
    if var < 1e-5: var = 1e-5
    return (1.0 / np.sqrt(2 * np.pi * var)) * np.exp(-((x - media)**2) / (2 * var))

def algoritmo_EM_GMM_1D(X, k=2, max_iter=50):
    """
    Algoritmo EM para 2 clusters Gaussianos en 1D.
    """
    # 1. Inicialización (aleatoria)
    n = len(X)
    # Adivinamos medias iniciales
    medias = np.random.choice(X, k)
    # Adivinamos varianzas iniciales
    varianzas = np.array([np.var(X)] * k)
    # Adivinamos pesos de mezcla (P(Cluster))
    pesos_mezcla = np.array([1/k] * k)
    
    # Responsabilidades (matriz n_muestras x k_clusters)
    resp = np.zeros((n, k))
    
    print(f"Medias iniciales: {medias}")

    # 4. Repetir
    for _ in range(max_iter):
        
        # --- 2. PASO E (Expectation) ---
        # Calcular responsabilidades: P(Cluster | dato)
        for i in range(n):
            for c in range(k):
                # P(dato | Cluster_c) * P(Cluster_c)
                resp[i, c] = pdf_gaussiana(X[i], medias[c], varianzas[c]) * pesos_mezcla[c]
            
            # Normalizar para que sum(resp[i, :]) == 1
            suma_resp_i = np.sum(resp[i, :])
            if suma_resp_i > 0:
                resp[i, :] /= suma_resp_i

        # --- 3. PASO M (Maximization) ---
        # Actualizar parámetros usando las responsabilidades
        
        # Suma de responsabilidades por cluster (N_c)
        N_c = np.sum(resp, axis=0)
        
        for c in range(k):
            # Nuevo peso de mezcla = N_c / N_total
            pesos_mezcla[c] = N_c[c] / n
            
            # Nueva media = (Suma(resp_ic * x_i)) / N_c
            suma_ponderada = np.dot(resp[:, c], X)
            medias[c] = suma_ponderada / N_c[c]
            
            # Nueva varianza = (Suma(resp_ic * (x_i - media_c)^2)) / N_c
            dif_cuadrada = (X - medias[c])**2
            var_ponderada = np.dot(resp[:, c], dif_cuadrada)
            varianzas[c] = var_ponderada / N_c[c]
            
    print(f"Medias finales: {medias}")
    print(f"Varianzas finales: {varianzas}")
    return medias, varianzas, pesos_mezcla

# --- Ejecución ---
# Datos: Dos grupos de números, uno alrededor de 20, otro de 80
X_grupo1 = np.random.normal(20, 5, 100)
X_grupo2 = np.random.normal(80, 10, 100)
X_datos = np.concatenate((X_grupo1, X_grupo2))
np.random.shuffle(X_datos)

print("Ejecutando EM para encontrar 2 clusters...")
algoritmo_EM_GMM_1D(X_datos, k=2)
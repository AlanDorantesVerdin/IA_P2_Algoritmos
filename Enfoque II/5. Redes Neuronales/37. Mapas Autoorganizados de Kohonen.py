# Algoritmo 37. Mapas Autoorganizados de Kohonen
# Alan Dorantes Verdin

import numpy as np

# (Usamos distancia_euclidiana de el Algoritmo 26)

def distancia_euclidiana(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.sqrt(np.sum((p1 - p2)**2))

def som_entrenar(X, map_size, epochs, tasa_aprendizaje_inicial, radio_inicial):
    """
    Entrena un Mapa Autoorganizado (SOM) 1D (para simplicidad).
    """
    n_muestras, n_features = X.shape
    n_neuronas = map_size[0] # Usamos un mapa 1D (una línea de neuronas)
    
    # 1. Inicializar pesos (mapa)
    # Cada neurona tiene un vector de pesos del tamaño de las features
    mapa_pesos = np.random.rand(n_neuronas, n_features)
    
    # Coordenadas 1D de las neuronas (0, 1, 2, 3...)
    neurona_idx = np.arange(n_neuronas)

    for epoch in range(epochs):
        # 2a. Tomar un dato de entrada
        x = X[np.random.randint(0, n_muestras)]
        
        # 2b. Encontrar la BMU (Best Matching Unit)
        distancias = [distancia_euclidiana(x, w) for w in mapa_pesos]
        bmu_idx = np.argmin(distancias)
        
        # Reducir tasa de aprendizaje y radio con el tiempo
        tasa_actual = tasa_aprendizaje_inicial * (1 - epoch / epochs)
        radio_actual = radio_inicial * (1 - epoch / epochs)
        
        # 2c. Actualizar pesos de BMU y vecinos
        for i in range(n_neuronas):
            w_i = mapa_pesos[i]
            dist_a_bmu = np.abs(i - bmu_idx) # Distancia en el mapa 1D
            
            # 2d. Calcular influencia de vecindad (Gaussiana)
            if dist_a_bmu <= radio_actual:
                influencia = np.exp(-(dist_a_bmu**2) / (2 * (radio_actual**2)))
                
                # Actualizar peso
                delta_w = tasa_actual * influencia * (x - w_i)
                mapa_pesos[i] += delta_w
                
    return mapa_pesos

# --- Ejecución ---
# Datos: Colores (R, G, B) para organizar
# 0=Rojo, 1=Verde, 2=Azul, 3=Amarillo, 4=Morado
X_colores = np.array([
    [1.0, 0.0, 0.0], [0.8, 0.1, 0.0], # Rojos
    [0.0, 1.0, 0.0], [0.1, 0.9, 0.1], # Verdes
    [0.0, 0.0, 1.0], [0.0, 0.1, 0.8], # Azules
    [1.0, 1.0, 0.0], [0.9, 0.8, 0.1]  # Amarillos
])

# Mapa 1D con 5 neuronas (para 4-5 grupos de color)
map_size_1d = (5,) 
mapa_final = som_entrenar(X_colores, map_size_1d, epochs=500, 
                          tasa_aprendizaje_inicial=0.5, radio_inicial=2.0)

print("\n--- 37. Mapas Autoorganizados de Kohonen (SOM) ---")
print("Mapa de pesos (neuronas) 1D final:")
print(mapa_final.round(2))
# (Se deberían ver neuronas especializadas en R, G, B, Y)
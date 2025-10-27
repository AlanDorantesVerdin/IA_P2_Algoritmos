# Algoritmo 21. Red Bayesiana Dinámica - Filtrado de Partículas
# Alan Dorantes Verdin

import numpy as np

print("\n--- 21. Red Bayesiana Dinámica - Filtrado de Partículas ---")

# --- El Modelo (DBN 1D simple) ---
# X_t = X_{t-1} + Ruido_Proceso  (Modelo de Transición/Movimiento)
# E_t = X_t     + Ruido_Sensor   (Modelo de Emisión/Observación)
# 
# Usamos ruido Gaussiano (Normal)
std_movimiento = 1.0 # Incertidumbre en el movimiento
std_sensor = 3.0     # Incertidumbre en la medición

def pdf_gaussiana(x, mu, sigma):
    """Calcula la 'probabilidad' (densidad) de x en N(mu, sigma^2)"""
    # Fórmula: 1/sqrt(2*pi*sigma^2) * exp( -(x-mu)^2 / (2*sigma^2) )
    if sigma == 0: return 1.0 if x == mu else 0.0
    var = sigma**2
    denom = np.sqrt(2 * np.pi * var)
    num = np.exp(-(x - mu)**2 / (2 * var))
    return num / denom


# --- ALGORITMO FILTRO DE PARTÍCULAS (SIR) ---
def filtro_particulas_sir(observaciones, N_particulas):
    """
    Estima la posición 1D usando un filtro de partículas SIR.
    """
    
    # --- 1. Inicialización ---
    # Creamos N partículas (hipótesis) alrededor de la primera observación
    posicion_inicial = observaciones[0]
    particulas = np.random.normal(posicion_inicial, std_sensor, N_particulas)
    pesos = np.ones(N_particulas) / N_particulas # Pesos iguales
    
    # Guardamos la estimación (media de las partículas) en cada paso
    estimaciones = [np.mean(particulas)]

    # --- 2. Bucle (para t=1, 2, ...) ---
    for t in range(1, len(observaciones)):
        
        # --- a. Predicción (Muestreo de Transición) ---
        # Movemos cada partícula según el modelo de movimiento (Transición)
        # Xt = Xt-1 + Ruido
        ruido_mov = np.random.normal(0, std_movimiento, N_particulas)
        particulas = particulas + ruido_mov
        
        # --- b. Ponderación (Actualización) ---
        # Pesamos cada partícula según qué tan bien explica la observación
        # peso_i = P(Et | X_t=particula_i)
        
        # Usamos la PDF gaussiana del sensor
        for i in range(N_particulas):
            pesos[i] = pdf_gaussiana(observaciones[t], particulas[i], std_sensor)
            
        # Normalizamos los pesos para que sumen 1
        suma_pesos = np.sum(pesos)
        if suma_pesos == 0:
            # Si todas las partículas son imposibles, reiniciamos
            pesos = np.ones(N_particulas) / N_particulas
        else:
            pesos = pesos / suma_pesos
            
        # --- c. Re-muestreo (Resampling) ---
        # Duplicamos partículas con peso alto, eliminamos las de peso bajo
        # (Muestreamos N veces del conjunto actual, usando los pesos)
        
        indices_remuestreados = np.random.choice(
            a=np.arange(N_particulas), # Índices [0, 1, ..., N-1]
            size=N_particulas,         # Queremos N nuevas partículas
            p=pesos,                   # Con probabilidad 'pesos'
            replace=True
        )
        
        # El nuevo conjunto de partículas es:
        particulas = particulas[indices_remuestreados]
        
        # Los pesos se resetean a 1/N después del re-muestreo
        pesos = np.ones(N_particulas) / N_particulas
        
        # Guardamos la estimación actual (la media de la nube de partículas)
        estimaciones.append(np.mean(particulas))
        
    return estimaciones

# --- EJECUCIÓN ---
# Simulación: El objeto se mueve de 0 a 10
posicion_real = np.arange(0, 11, 1) # [0, 1, 2, ..., 10]

# Generamos observaciones ruidosas (el GPS es impreciso)
obs_ruidosas = posicion_real + np.random.normal(0, std_sensor, len(posicion_real))

# Ejecutamos el filtro
N = 1000
estimaciones_filtro = filtro_particulas_sir(obs_ruidosas, N)

print(f"--- Filtro de Partículas (N={N}) ---")
print("T (Paso) | Real | Observación | Estimación (Filtro)")
print("-" * 45)
for t in range(len(posicion_real)):
    print(f"t={t:<7} | {posicion_real[t]:<4.1f} | {obs_ruidosas[t]:<11.2f} | {estimaciones_filtro[t]:<10.2f}")
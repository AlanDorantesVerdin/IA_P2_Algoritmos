# Algoritmo 20. Filtros de Kalman
# Alan Dorantes Verdin

print("\n--- 20. Filtros de Kalman ---")

import numpy as np

class KalmanFilter2D:
    """
    Implementación simple de un Filtro de Kalman 2D para rastrear
    posición (x, y) y velocidad (vx, vy).
    """
    
    def __init__(self, dt, std_proceso, std_medida):
        """
        Inicializa el filtro.
        :param dt:          Intervalo de tiempo (ej. 0.1 segundos)
        :param std_proceso: Desviación estándar del ruido del proceso (Q)
                            (Cuánto confiamos en el modelo de movimiento)
        :param std_medida:  Desviación estándar del ruido de medida (R)
                            (Cuánto confiamos en el sensor)
        """
        
        self.dt = dt
        
        # --- Matriz de Transición de Estado (F) ---
        # Define cómo el estado evoluciona del tiempo t-1 a t
        # (Modelo de movimiento a velocidad constante)
        # x_t = x_{t-1} + vx_{t-1} * dt
        # y_t = y_{t-1} + vy_{t-1} * dt
        # vx_t = vx_{t-1}
        # vy_t = vy_{t-1}
        self.F = np.array([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # --- Matriz de Observación (H) ---
        # Define cómo el estado se mapea a una observación
        # (Solo medimos la posición x, y)
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        # --- Covarianza del Ruido del Proceso (Q) ---
        # Incertidumbre en el modelo de movimiento (ej. aceleraciones 
        # inesperadas).
        # Se asume que el ruido es independiente en x, y.
        q_val = std_proceso**2
        self.Q = np.array([
            [q_val, 0, 0, 0],
            [0, q_val, 0, 0],
            [0, 0, q_val, 0],
            [0, 0, 0, q_val]
        ])

        # --- Covarianza del Ruido de Medida (R) ---
        # Incertidumbre de nuestro sensor.
        r_val = std_medida**2
        self.R = np.array([
            [r_val, 0],
            [0, r_val]
        ])

        # --- Estado Inicial (x) y Covarianza (P) ---
        # [x, y, vx, vy].T (Vector columna 4x1)
        # Empezamos en (0,0) con velocidad (0,0)
        self.x = np.zeros((4, 1))
        
        # Incertidumbre inicial (P)
        # Empezamos con una incertidumbre muy alta
        self.P = np.eye(4) * 1000.0 


    def predict(self):
        """
        Paso de PREDICCIÓN.
        Proyecta el estado y la covarianza hacia adelante en el tiempo.
        x_pred = F * x
        P_pred = F * P * F^T + Q
        """
        
        # x = F * x
        # Usamos np.dot para multiplicación de matrices
        self.x = np.dot(self.F, self.x)
        
        # P = F * P * F^T + Q
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        
        # Devolvemos la posición predicha
        return self.x[0:2] # Devuelve [x, y]


    def update(self, z):
        """
        Paso de ACTUALIZACIÓN (Corrección).
        Corrige la predicción usando la nueva medición 'z'.
        :param z: Medición actual [x_medido, y_medido].T (Vector columna 2x1)
        """
        
        # --- 1. Calcular la Ganancia de Kalman (K) ---
        
        # y = z - H * x_pred (Innovación o error de medida)
        y = z - np.dot(self.H, self.x)
        
        # S = H * P_pred * H^T + R (Covarianza de la innovación)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        
        # K = P_pred * H^T * S^{-1} (Ganancia de Kalman)
        # np.linalg.inv() es la inversa de una matriz
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        
        
        # --- 2. Actualizar el estado (x) y la covarianza (P) ---
        
        # x_actual = x_pred + K * y
        self.x = self.x + np.dot(K, y)
        
        # P_actual = (I - K * H) * P_pred
        I = np.eye(4) # Matriz identidad
        self.P = np.dot(I - np.dot(K, self.H), self.P)
        
        # Devolvemos la posición actualizada
        return self.x[0:2] # Devuelve [x, y]


# --- EJECUCIÓN DEL EJEMPLO ---

# 1. Simular datos reales
dt = 0.1
num_pasos = 100
# El objeto real se mueve en línea recta con velocidad (1, 0.5)
velocidad_real = np.array([1.0, 0.5])
posicion_real = np.zeros((num_pasos, 2))
for t in range(1, num_pasos):
    posicion_real[t] = posicion_real[t-1] + velocidad_real * dt

# 2. Simular mediciones ruidosas
std_medida = 3.0
# Generamos ruido gaussiano y lo sumamos a la posición real
ruido = np.random.normal(0, std_medida, (num_pasos, 2))
mediciones = posicion_real + ruido

# 3. Inicializar y ejecutar el Filtro de Kalman
std_proceso = 0.1 # Le decimos al filtro que confiamos bastante en el modelo
kf = KalmanFilter2D(dt=dt, std_proceso=std_proceso, std_medida=std_medida)

estimaciones_kf = np.zeros((num_pasos, 2))

print("Ejecutando Filtro de Kalman 2D...")
print("-" * 60)
print(f"{'Paso':<5} | {'Medición (x, y)':<20} | {'Estimación KF (x, y)':<25}")
print("-" * 60)

for t in range(num_pasos):
    # Convertir la medición a un vector columna (2x1)
    z_t = mediciones[t].reshape(2, 1)
    
    # 1. Predecir
    kf.predict()
    
    # 2. Actualizar
    estimacion = kf.update(z_t)
    
    # Guardar la estimación (aplanándola a 1D)
    estimaciones_kf[t] = estimacion.flatten()
    
    if t % 10 == 0: # Imprimir cada 10 pasos
        med_str = f"({mediciones[t, 0]:.2f}, {mediciones[t, 1]:.2f})"
        est_str = f"({estimaciones_kf[t, 0]:.2f}, {estimaciones_kf[t, 1]:.2f})"
        print(f"{t:<5} | {med_str:<20} | {est_str:<25}")

# 4. Calcular el error
# RMSE verdadero (raíz del promedio del error cuadrático por muestra)
error_medicion = np.sqrt(np.mean(np.sum((mediciones - posicion_real)**2, axis=1)))
error_kf = np.sqrt(np.mean(np.sum((estimaciones_kf - posicion_real)**2, axis=1)))

print("-" * 60)
print(f"Error cuadrático medio (RMSE) de la Medición: {error_medicion:.4f}")
print(f"Error cuadrático medio (RMSE) del Filtro de Kalman: {error_kf:.4f}")
print("\nEl Filtro de Kalman (Estimación KF) produce un error mucho menor")
print("que las mediciones ruidosas directas.")
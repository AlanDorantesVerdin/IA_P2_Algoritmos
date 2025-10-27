# Algoritmo 29. Máquinas de Vectores de Soporte (Núcleo)
# Alan Dorantes Verdin

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np

# --- Ejecución SVM ---
# (Datos de Naive Bayes)
X_svm = np.array([[180, 85], [175, 75], [185, 90], [160, 55], [165, 60], [170, 65]])
y_svm = np.array([0, 0, 0, 1, 1, 1]) # 0=Hombre, 1=Mujer

# Las SVM son sensibles a la escala de los datos, por lo que escalamos
scaler = StandardScaler()
X_svm_esc = scaler.fit_transform(X_svm)

# 1. Crear el modelo SVM
# C=1.0 es el parámetro de regularización
# kernel='linear' (separador lineal)
# kernel='rbf' (núcleo Gaussiano, no lineal - este es el más común)
modelo_svm = SVC(kernel='linear', C=1.0)

# 2. Entrenar el modelo
modelo_svm.fit(X_svm_esc, y_svm)

# 3. Predecir un dato nuevo
# (Dato: [168, 60])
x_nuevo_svm = np.array([[168, 60]])
# Debemos escalar el dato nuevo igual que los datos de entrenamiento
x_nuevo_svm_esc = scaler.transform(x_nuevo_svm)

pred_svm = modelo_svm.predict(x_nuevo_svm_esc)

print(f"\n--- 29. Máquinas de Vectores Soporte (SVM) ---")
print(f"Punto nuevo (escalado): {x_nuevo_svm_esc[0]}")
print(f"Predicción (kernel='linear'): {pred_svm[0]} (1=Mujer)")
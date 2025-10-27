# Algoritmo 24. Naive Bayes
# Alan Dorantes Verdin

print("\n--- 24. Naive Bayes ---")

import numpy as np

class GaussianNaiveBayes:
    """Implementación simple de Gaussian Naive Bayes."""
    
    def __init__(self):
        self.clases_info = {} # Almacena (media, var, previa) por clase
        self.clases = []

    def fit(self, X, y):
        """
        Entrena el modelo.
        X: (n_muestras, n_features) array de características
        y: (n_muestras,) array de etiquetas de clase
        """
        self.clases = np.unique(y)
        
        for clase in self.clases:
            # 1. Separar los datos por clase
            X_clase = X[y == clase]
            
            # 2. Calcular media, varianza por feature, y previa por clase
            media = np.mean(X_clase, axis=0)
            varianza = np.var(X_clase, axis=0)
            previa = len(X_clase) / len(X)
            
            # Guardar la información
            self.clases_info[clase] = (media, varianza, previa)

    def _pdf_gaussiana(self, x, media, var):
        """Calcula la Densidad de Probabilidad (PDF) Gaussiana."""
        # Evitar división por cero si la varianza es 0
        if var == 0: var = 1e-4 
            
        exponente = -((x - media)**2) / (2 * var)
        denominador = np.sqrt(2 * np.pi * var)
        return np.exp(exponente) / denominador

    def predict(self, X):
        """Predice la clase para un conjunto de datos X."""
        predicciones = []
        for x_fila in X:
            # Calcular la prob. posterior para CADA clase
            posteriores = []
            
            for clase in self.clases:
                media, varianza, previa = self.clases_info[clase]
                
                # P(Clase) * Producto( P(feature_i | Clase) )
                posterior = np.log(previa) # Usamos log-prob para evitar underflow
                
                # Sumamos los logaritmos (equivale a multiplicar probabilidades)
                for i in range(len(x_fila)):
                    prob_feature_dado_clase = self._pdf_gaussiana(x_fila[i], media[i], varianza[i])
                    posterior += np.log(prob_feature_dado_clase + 1e-9) # +1e-9 para evitar log(0)
                
                posteriores.append(posterior)
                
            # Elegir la clase con la prob. posterior más alta
            predicciones.append(self.clases[np.argmax(posteriores)])
            
        return np.array(predicciones)

# --- Ejecución ---
# Datos: Altura (cm) y Peso (kg) para 'Hombre' (0) y 'Mujer' (1)
X_ent = np.array([
    [180, 85], [175, 75], [185, 90], # Hombres
    [160, 55], [165, 60], [170, 65]  # Mujeres
])
y_ent = np.array([0, 0, 0, 1, 1, 1])

modelo_nb = GaussianNaiveBayes()
modelo_nb.fit(X_ent, y_ent)

# Dato nuevo: [178 cm, 70 kg] (¿Hombre o Mujer?)
X_nuevo = np.array([[178, 70]])
prediccion = modelo_nb.predict(X_nuevo)

print(f"Datos de entrenamiento (Altura, Peso): \n{X_ent}")
print(f"Etiquetas: {y_ent} (0=Hombre, 1=Mujer)")
print(f"\nDato a predecir: {X_nuevo[0]}")
print(f"Predicción de Naive Bayes: {prediccion[0]}")
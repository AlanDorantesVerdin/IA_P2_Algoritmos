# Algoritmo 30. Aprendizaje Profundo (Deep Learning)
# Alan Dorantes Verdin

import numpy as np

# --- 1. Componentes (Activación) ---
def sigmoid(x):
    """Función de activación Sigmoid."""
    return 1 / (1 + np.exp(-x))

def derivada_sigmoid(x):
    """Derivada de la función Sigmoid (usada en backpropagation)."""
    fx = sigmoid(x)
    return fx * (1 - fx)

# --- 2. Algoritmo Red Neuronal (MLP) ---

class MLP_para_XOR:
    
    def __init__(self):
        # 1. Definir Arquitectura
        self.n_entrada = 2
        self.n_oculta = 2 # Capa oculta "profunda"
        self.n_salida = 1
        
        # 2. Inicializar Pesos (Aleatoriamente)
        np.random.seed(42)
        # Pesos: Capa de Entrada -> Capa Oculta
        self.pesos_oculta = np.random.rand(self.n_entrada, self.n_oculta)
        # Pesos: Capa Oculta -> Capa de Salida
        self.pesos_salida = np.random.rand(self.n_oculta, self.n_salida)

    def forward_pass(self, X):
        """Pasa los datos hacia adelante por la red."""
        # Entrada -> Oculta
        self.z_oculta = np.dot(X, self.pesos_oculta)
        self.a_oculta = sigmoid(self.z_oculta)
        
        # Oculta -> Salida
        self.z_salida = np.dot(self.a_oculta, self.pesos_salida)
        self.a_salida = sigmoid(self.z_salida)
        
        return self.a_salida # Predicción

    def backward_pass(self, X, y, prediccion, tasa_aprendizaje):
        """
        Paso de Retropropagación (Backpropagation)
        (Este es el núcleo de Deep Learning)
        """
        
        # --- 1. Calcular Error en la Capa de Salida ---
        error_salida = y - prediccion
        # d_cost/d_z_salida = d_cost/d_a_salida * d_a_salida/d_z_salida
        # d_cost/d_a_salida = (a_salida - y)
        # d_a_salida/d_z_salida = derivada_sigmoid(z_salida)
        # (Nota: Para Error Cuadrático Medio, el error_salida es d_cost/d_a_salida)
        d_salida = error_salida * derivada_sigmoid(self.z_salida)

        # --- 2. Calcular Error en la Capa Oculta ---
        # Propagar el error hacia atrás
        error_oculta = np.dot(d_salida, self.pesos_salida.T)
        d_oculta = error_oculta * derivada_sigmoid(self.z_oculta)

        # --- 3. Calcular Gradientes (d_cost / d_pesos) ---
        # Gradiente Pesos Salida:
        grad_pesos_salida = np.dot(self.a_oculta.T, d_salida)
        # Gradiente Pesos Oculta:
        grad_pesos_oculta = np.dot(X.T, d_oculta)

        # --- 4. Actualizar Pesos (Descenso de Gradiente) ---
        self.pesos_salida += grad_pesos_salida * tasa_aprendizaje
        self.pesos_oculta += grad_pesos_oculta * tasa_aprendizaje

    def entrenar(self, X, y, epochs, tasa_aprendizaje):
        """Bucle de entrenamiento."""
        for epoch in range(epochs):
            # Forward pass
            prediccion = self.forward_pass(X)
            
            # Backward pass (Backpropagation)
            self.backward_pass(X, y, prediccion, tasa_aprendizaje)
            
            if epoch % 1000 == 0:
                # Calculamos la pérdida (Error Cuadrático Medio)
                loss = np.mean(np.square(y - prediccion))
                print(f"Epoch {epoch}: Pérdida = {loss:.4f}")

# --- Ejecución ---
# Datos: El problema XOR
X_xor = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
# Etiquetas XOR
y_xor = np.array([
    [0],
    [1],
    [1],
    [0]
])

# Crear y entrenar la red
red_neuronal = MLP_para_XOR()
print("\n--- 30. Aprendizaje Profundo (MLP para XOR) ---")
red_neuronal.entrenar(X_xor, y_xor, epochs=10000, tasa_aprendizaje=0.1)

# Probar la red entrenada
print("\nPredicciones finales:")
predicciones_finales = red_neuronal.forward_pass(X_xor)
for i in range(len(X_xor)):
    print(f"Entrada: {X_xor[i]} -> Salida: {predicciones_finales[i][0]:.4f} (Esperado: {y_xor[i][0]})")
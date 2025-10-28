# Algoritmo 48. Texturas y Sombras
# Alan Dorantes Verdin

import numpy as np

def sombreado_lambertiano(normal_superficie, direccion_luz, intensidad_luz=1.0):
    """
    Calcula el brillo de una superficie usando el modelo Lambertiano.
    """
    # 1. Normalizar vectores (para que tengan longitud 1)
    N = normal_superficie / np.linalg.norm(normal_superficie)
    L = direccion_luz / np.linalg.norm(direccion_luz)
    
    # 2. Calcular el producto punto
    # (cos(theta) = N . L)
    cos_theta = np.dot(N, L)
    
    # 3. Asegurarse de que el brillo no sea negativo
    # (Si cos_theta es < 0, la luz está "detrás" de la superficie)
    intensidad = max(0, cos_theta)
    
    # 4. Aplicar intensidad de la luz
    brillo_final = intensidad_luz * intensidad
    
    return brillo_final

# --- Ejecución ---
print("\n--- 48. Sombreado Lambertiano ---")

# La luz viene desde arriba a la derecha (x=1, y=1)
luz = np.array([1.0, 1.0, 0.0]) 

# Caso 1: Superficie mirando directo a la luz
normal_1 = np.array([1.0, 1.0, 0.0]) # Misma dirección que la luz
brillo_1 = sombreado_lambertiano(normal_1, luz)
print(f"Superficie 1 (mira a la luz):   Brillo = {brillo_1:.2f} (Máximo)")

# Caso 2: Superficie mirando de lado
normal_2 = np.array([-1.0, 1.0, 0.0]) # 90 grados
brillo_2 = sombreado_lambertiano(normal_2, luz)
print(f"Superficie 2 (mira de lado):    Brillo = {brillo_2:.2f} (Medio)")

# Caso 3: Superficie mirando en contra
normal_3 = np.array([-1.0, -1.0, 0.0]) # Opuesta
brillo_3 = sombreado_lambertiano(normal_3, luz)
print(f"Superficie 3 (mira en contra): Brillo = {brillo_3:.2f} (Oscuro)")
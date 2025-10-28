# Algoritmo 46. Preprocesado - Filtros
# Alan Dorantes Verdin

import numpy as np

def filtro_gaussiano(imagen, kernel):
    """
    Aplica un filtro de convolución (como un desenfoque Gaussiano).
    """
    img_alto, img_ancho = imagen.shape
    k_alto, k_ancho = kernel.shape
    
    # Relleno (padding) para manejar los bordes
    # (Calculamos cuánto relleno se necesita)
    pad_h = k_alto // 2
    pad_w = k_ancho // 2
    
    # Crear imagen con relleno (bordes con 0)
    img_rellenada = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), 'constant')
    img_filtrada = np.zeros_like(imagen)

    # --- Bucle de Convolución ---
    for y in range(img_alto):
        for x in range(img_ancho):
            # Extraer la "vecindad" (el trozo de imagen bajo el kernel)
            vecindad = img_rellenada[y : y + k_alto, x : x + k_ancho]
            
            # Aplicar el kernel: Suma(vecindad * kernel)
            valor_filtrado = np.sum(vecindad * kernel)
            img_filtrada[y, x] = valor_filtrado
            
    return img_filtrada

# --- Ejecución ---
print("\n--- 46. Preprocesado: Filtros (Gaussiano) ---")

# 1. Una imagen simple (un punto blanco sobre fondo negro)
imagen_ruido = np.zeros((7, 7), dtype=int)
imagen_ruido[3, 3] = 100 # Un píxel brillante

# 2. Un kernel Gaussiano simple (normalizado para que sume ~1)
kernel_gauss = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]) / 16.0

print("Imagen Original (con 'ruido'):")
print(imagen_ruido)

imagen_suavizada = filtro_gaussiano(imagen_ruido, kernel_gauss)

print("\nImagen Suavizada (desenfocada):")
print(imagen_suavizada.round(1))
# Algoritmo 49. Reconocimiento de Objetos
# Alan Dorantes Verdin

import numpy as np

def coincidencia_plantillas_ssd(imagen, plantilla):
    """
    Encuentra la plantilla en la imagen usando Suma de Diferencias 
    al Cuadrado (SSD).
    """
    img_h, img_w = imagen.shape
    plt_h, plt_w = plantilla.shape
    
    # 'mapa_costo' almacenará el costo SSD en cada posición (x, y)
    mapa_costo = np.zeros((img_h - plt_h, img_w - plt_w))
    
    # 2. Deslizar la plantilla
    for y in range(img_h - plt_h):
        for x in range(img_w - plt_w):
            
            # 3. Extraer la ventana de la imagen
            ventana = imagen[y : y + plt_h, x : x + plt_w]
            
            # 3. Calcular costo SSD
            diferencia = ventana - plantilla
            costo_ssd = np.sum(diferencia**2)
            
            mapa_costo[y, x] = costo_ssd
            
    # 4. Encontrar la posición con el costo MÍNIMO
    # (np.unravel_index convierte el índice lineal (argmin) en (y, x))
    mejor_y, mejor_x = np.unravel_index(np.argmin(mapa_costo), mapa_costo.shape)
    
    return (mejor_y, mejor_x)

# --- Ejecución ---
print("\n--- 49. Reconocimiento de Objetos (Template Matching) ---")

# 1. Imagen grande
imagen_grande = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 5, 5, 0, 0, 0],
    [0, 5, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

# 2. Plantilla (el objeto 2x2 que buscamos)
plantilla = np.array([
    [5, 5],
    [5, 5]
])

print("Imagen Grande:")
print(imagen_grande)
print("\nPlantilla (Objeto a buscar):")
print(plantilla)

(y, x) = coincidencia_plantillas_ssd(imagen_grande, plantilla)
print(f"\nObjeto encontrado en la posición (y, x): ({y}, {x})")
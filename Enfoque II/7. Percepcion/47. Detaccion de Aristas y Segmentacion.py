# Algoritmo 47. Detección de Aristas y Segmentación
# Alan Dorantes Verdin

import numpy as np

# Funciones de Dibujo y Filtros (de algoritmos previos)

def dda_linea(x1, y1, x2, y2, ancho, alto):
    """
    Dibuja una línea en un 'lienzo' (array) usando DDA.
    """
    # Crear un lienzo vacío (array de ceros)
    lienzo = np.zeros((alto, ancho), dtype=int)
    
    # 1. Calcular dx, dy
    dx = x2 - x1
    dy = y2 - y1
    
    # 2. Determinar el número de pasos
    if abs(dx) > abs(dy):
        pasos = abs(dx)
    else:
        pasos = abs(dy)
    
    if pasos == 0:
        if 0 <= x1 < ancho and 0 <= y1 < alto:
             lienzo[y1, x1] = 1
        return lienzo

    # 3. Calcular el incremento (delta) para x e y
    inc_x = dx / pasos
    inc_y = dy / pasos
    
    # 4. Bucle de dibujo
    x, y = float(x1), float(y1)
    for _ in range(int(pasos) + 1):
        # Redondear para obtener el píxel más cercano
        px, py = int(round(x)), int(round(y))
        
        # Dibujar si está dentro de los límites
        if 0 <= px < ancho and 0 <= py < alto:
            lienzo[py, px] = 1
            
        # Incrementar para el siguiente paso
        x += inc_x
        y += inc_y
        
    return lienzo

def imprimir_lienzo_ascii(lienzo):
    """Convierte el array numérico en arte ASCII."""
    print("--- Lienzo ASCII ---")
    for fila in lienzo:
        linea_str = ""
        for pixel in fila:
            linea_str += "# " if pixel == 1 else ". "
        print(linea_str)
    print("--------------------")

# (Usamos la función filtro_gaussiano de arriba como 'convolucion')

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

def detector_aristas_sobel(imagen):
    """
    Detecta aristas usando el operador Sobel.
    """
    # 1. Kernels de Sobel
    Kx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    
    Ky = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ])
    
    # 2. Aplicar convolución
    Gx = filtro_gaussiano(imagen, Kx)
    Gy = filtro_gaussiano(imagen, Ky)
    
    # 3. Calcular Magnitud (simplificado como |Gx| + |Gy|)
    # (Usar sqrt(Gx**2 + Gy**2) es más preciso pero más lento)
    G_magnitud = np.abs(Gx) + np.abs(Gy)
    
    return G_magnitud

def segmentacion_por_umbral(imagen, umbral):
    """
    Segmenta una imagen: 1 si (pixel > umbral), 0 si no.
    """
    # np.where es una forma rápida de hacer el if/else
    imagen_segmentada = np.where(imagen > umbral, 1, 0)
    return imagen_segmentada

# --- Ejecución ---
print("\n--- 47. Detección de Aristas (Sobel) y Segmentación ---")

# 1. Imagen simple (un "cuadrado")
imagen_cuadrado = np.zeros((7, 7))
imagen_cuadrado[2:5, 2:5] = 100 # Un cuadrado 3x3 de 100s

print("Imagen Original (Cuadrado):")
print(imagen_cuadrado)

# 2. Detección de Aristas
imagen_aristas = detector_aristas_sobel(imagen_cuadrado)
print("\nAristas (Sobel):")
print(imagen_aristas.round(0))

# 3. Segmentación (Umbralización) de las aristas
umbral = 50
imagen_segmentada = segmentacion_por_umbral(imagen_aristas, umbral)
print("\nAristas Segmentadas (Umbral > 50):")
imprimir_lienzo_ascii(imagen_segmentada)
# Algoritmo 52. Movimiento
# Alan Dorantes Verdin

import numpy as np

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

def resta_de_fotogramas(frame_anterior, frame_actual, umbral):
    """
    Detecta movimiento usando resta de fotogramas y umbralización.
    """
    
    # 1. Calcular diferencia absoluta
    # (Asegurarse de que sean del mismo tipo, ej. float)
    diff = np.abs(frame_actual.astype(float) - frame_anterior.astype(float))
    
    # 2. Aplicar umbral
    mapa_movimiento = np.where(diff > umbral, 1, 0)
    
    return mapa_movimiento

# --- Ejecución ---
print("\n--- 52. Movimiento (Resta de Fotogramas) ---")

# 1. Fotograma anterior (un objeto a la izquierda)
frame_t_menos_1 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

# 2. Fotograma actual (el objeto se movió a la derecha)
frame_t = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
])

umbral_movimiento = 0.5
mapa_mov = resta_de_fotogramas(frame_t_menos_1, frame_t, umbral_movimiento)

print("Fotograma Anterior (t-1):")
imprimir_lienzo_ascii(frame_t_menos_1)
print("Fotograma Actual (t):")
imprimir_lienzo_ascii(frame_t)
print("Mapa de Movimiento (Diferencia > 0.5):")
imprimir_lienzo_ascii(mapa_mov)
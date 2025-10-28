# Algoritmo 45. Gráficos por Computador
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

# --- Ejecución ---
print("\n--- 45. Gráficos por Computador (Línea DDA) ---")
# Dibujar una línea de (2, 2) a (18, 7) en un lienzo de 20x10
lienzo_linea = dda_linea(2, 2, 18, 7, 20, 10)
imprimir_lienzo_ascii(lienzo_linea)
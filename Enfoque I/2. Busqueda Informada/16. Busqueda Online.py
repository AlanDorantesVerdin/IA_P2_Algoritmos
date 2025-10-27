# Algoritmo 16. Búsqueda Online
# Alan Dorantes Verdin

import math
import random

# --- El Mundo (Grid) ---
# 0 = Abierto, 1 = Muro
GRID_WORLD = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
GRID_ANCHO = len(GRID_WORLD[0])
GRID_ALTO = len(GRID_WORLD)

INICIO = (0, 0)
OBJETIVO = (5, 5)

def es_valido(s):
    """Verifica si una coordenada (x, y) está dentro del grid y no es un muro."""
    x, y = s
    if 0 <= x < GRID_ANCHO and 0 <= y < GRID_ALTO:
        return GRID_WORLD[y][x] == 0
    return False

def get_vecinos_mundo(s):
    """Obtiene los vecinos válidos de un estado 's' en el MUNDO REAL."""
    x, y = s
    vecinos = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        vecino_s = (x + dx, y + dy)
        if es_valido(vecino_s):
            vecinos.append(vecino_s)
    return vecinos

def costo_movimiento(s1, s2):
    """Costo de moverse de s1 a s2 (siempre 1 en nuestro grid)."""
    return 1

# Heurística inicial (Distancia Manhattan)
def h_manhattan(s, objetivo):
    """Estima el costo desde 's' al 'objetivo' (no sabe de muros)."""
    return abs(s[0] - objetivo[0]) + abs(s[1] - objetivo[1])

class AgenteLRTA:
    """
    Este agente aprende mientras se mueve.
    No conoce el mapa, solo su 'H' (tabla de heurísticas aprendidas).
    """
    def __init__(self, mundo_real, objetivo):
        # El agente NO debe ver el 'mundo_real', pero lo usamos
        # para simular sus 'sensores' (get_vecinos_mundo).
        self.mundo_real = mundo_real 
        self.objetivo = objetivo
        
        # H es la memoria del agente.
        # Almacena el costo *aprendido* (o estimado) de 's' al objetivo.
        self.H = {} # {estado: costo_aprendido}
        
    def h_inicial(self, s):
        """Heurística inicial (Manhattan) si nunca hemos visto 's'."""
        return h_manhattan(s, self.objetivo)

    def get_H(self, s):
        """Obtiene el valor H de la memoria, o usa la h_inicial si es nuevo."""
        return self.H.get(s, self.h_inicial(s))

    def tomar_decision(self, estado_actual):
        """
        El núcleo de LRTA*:
        1. Mira a los vecinos.
        2. Calcula el costo A* (f = g + h) para cada uno.
        3. Actualiza H(estado_actual) con el mejor costo.
        4. Se mueve al mejor vecino.
        """
        
        if estado_actual == self.objetivo:
            return None # Ya llegamos

        # 1. El agente "mira" a su alrededor (simulamos sensores)
        # Esto es lo único que sabe del mundo en este paso.
        vecinos = get_vecinos_mundo(estado_actual)
        
        if not vecinos:
            # Atrapado en un callejón sin salida
            print(f"¡Atrapado en {estado_actual}! Actualizando H a infinito.")
            self.H[estado_actual] = float('inf')
            # (En un agente real, intentaría retroceder a un estado previo)
            return None # No se puede mover

        # 2. Calcular el costo f(n) para cada vecino 'v'
        # f(v) = costo(actual, v) + H(v)
        costos_f = []
        for vecino in vecinos:
            g = costo_movimiento(estado_actual, vecino) # Siempre 1
            h = self.get_H(vecino)                      # Valor H del vecino
            f = g + h
            costos_f.append((f, vecino))
            
        # 3. Encontrar el mejor vecino (el de menor costo f)
        mejor_f, mejor_vecino = min(costos_f, key=lambda x: x[0])
        
        # 4. Aprender: Actualizar la H del estado actual
        # "El costo para llegar al objetivo desde AQUÍ (estado_actual)
        # es el costo de ir a mi mejor vecino (mejor_f)."
        self.H[estado_actual] = mejor_f
        
        # 5. Devolver el estado al que el agente decide moverse
        return mejor_vecino

# --- Simulación de Búsqueda Online ---
print("\n--- 16. Búsqueda Online (LRTA*) ---")

# 1. Creamos el agente
agente = AgenteLRTA(GRID_WORLD, OBJETIVO)

# 2. Bucle de simulación
estado_actual = INICIO
camino_recorrido = [estado_actual]
max_pasos = 100 # Para evitar bucles infinitos si algo sale mal

for i in range(max_pasos):
    print(f"Paso {i}: Agente está en {estado_actual}. H({estado_actual}) = {agente.get_H(estado_actual):.2f}")
    
    # 3. El agente toma una decisión y devuelve su próximo movimiento
    proximo_estado = agente.tomar_decision(estado_actual)
    
    if proximo_estado is None:
        if estado_actual == OBJETIVO:
            print(f"\n¡Objetivo {OBJETIVO} alcanzado!")
        else:
            print("\nAgente atascado o finalizado sin llegar al objetivo.")
        break
        
    # 4. El agente se mueve
    estado_actual = proximo_estado
    camino_recorrido.append(estado_actual)
    
    if i == max_pasos - 1:
        print("\nLímite de pasos alcanzado.")

print(f"Camino total recorrido: {camino_recorrido}\n")
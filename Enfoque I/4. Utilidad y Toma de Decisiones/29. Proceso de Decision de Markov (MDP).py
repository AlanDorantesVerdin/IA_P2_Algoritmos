# Algoritmo 29. Proceso de Decisión de Markov (MDP)
# Alan Dorantes Verdin

# --- Definición del MDP (Mundo-Línea) ---

# 1. Estados
estados = [0, 1, 2, 3]
estados_terminales = [2, 3]

# 2. Acciones
acciones = ['izquierda', 'derecha']

# 3. Factor de Descuento
gamma = 0.9

# 4. Recompensas R(s')
recompensas = {
    0: 0,
    1: 0,
    2: -1, # Pozo
    3: 1   # Tesoro
}

# 5. Transiciones T(s, a) -> [(prob, s_siguiente), ...]
transiciones = {
    0: {
        'izquierda': [(0.8, 0), (0.2, 0)], # Choca con muro, 100% queda en 0
        'derecha':   [(0.8, 1), (0.2, 0)]  # 80% éxito, 20% fallo
    },
    1: {
        'izquierda': [(0.8, 0), (0.2, 1)],
        'derecha':   [(0.8, 2), (0.2, 1)]  # 80% va al pozo, 20% queda en 1
    },
    # Estados terminales: no tienen transiciones de salida
    2: {},
    3: {}
}

# --- Ejemplo de uso ---
print("\n--- 29. Proceso de Decisión de Markov (MDP) ---")
print("Concepto: Es el modelo formal (Estados, Acciones, Transiciones, Recompensas).")
print(f"Estados: {estados}")
print(f"Acciones: {acciones}")
print(f"MDP definido y listo para usar.\n")
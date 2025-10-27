# Algoritmo 15. Procesos Estacionarios
# Alan Dorantes Verdin

print("\n--- 15. Procesos Estacionarios ---")

# Un proceso estacionario tiene una matriz de transición fija.

# Estados: 0 = 'Sol', 1 = 'Lluvia'
# Matriz de transición P(Xt | Xt-1)
# Sol(t) Lluvia(t)
# Sol(t-1) [0.8,    0.2]
# Lluvia(t-1) [0.4,    0.6]
matriz_transicion = [
    [0.8, 0.2],  # Probabilidades desde 'Sol'
    [0.4, 0.6]   # Probabilidades desde 'Lluvia'
]

def obtener_prob_transicion(estado_anterior, estado_siguiente):
    """
    Devuelve P(estado_siguiente | estado_anterior)
    usando la matriz estacionaria.
    """
    # 0 = Sol, 1 = Lluvia
    idx_anterior = 0 if estado_anterior == 'Sol' else 1
    idx_siguiente = 0 if estado_siguiente == 'Sol' else 1
    
    return matriz_transicion[idx_anterior][idx_siguiente]

# El punto clave es que esta probabilidad NO depende del tiempo 't'
prob_t2 = obtener_prob_transicion('Sol', 'Lluvia') # P(X_2 = Lluvia | X_1 = Sol)
prob_t100 = obtener_prob_transicion('Sol', 'Lluvia') # P(X_100 = Lluvia | X_99 = Sol)

print(f"Prob. de 'Sol' a 'Lluvia' en t=2: {prob_t2}")
print(f"Prob. de 'Sol' a 'Lluvia' en t=100: {prob_t100}")
print("Son iguales porque el proceso es estacionario.")
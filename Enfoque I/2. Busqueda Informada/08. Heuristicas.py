# Algoritmo 08. Heurísticas
# Alan Dorantes Verdin

print("\n--- 8. Heurísticas ---")

# La heurística es una función o tabla. Usaremos la tabla definida:
heuristicas_hacia_F = { 'A': 10, 'B': 8, 'C': 9, 'D': 5, 'E': 3, 'F': 0 }

def h(nodo):
    """ Función heurística simple (h(n)) """
    # Devuelve el valor de la tabla, o 0 si no está (para el objetivo)
    return heuristicas_hacia_F.get(nodo, 0)

print(f"La heurística (costo estimado) desde 'A' hasta 'F' es: h('A') = {h('A')}")
print(f"La heurística (costo estimado) desde 'E' hasta 'F' es: h('E') = {h('E')}")
print(f"La heurística (costo estimado) desde 'F' hasta 'F' es: h('F') = {h('F')}\n")
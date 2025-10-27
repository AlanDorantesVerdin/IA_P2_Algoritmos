# Algoritmo 7. Red Bayesiana
# Alan Dorantes Verdin

print("\n--- 7. Red Bayesiana ---")

# Las Tablas de Probabilidad Condicionada (CPTs) definen la red.
# Usamos diccionarios anidados.
# Las claves 'T' y 'F' significan True (Verdadero) y False (Falso).

# P(N)
cpt_nublado = {
    'T': 0.5,
    'F': 0.5
}

# P(A | N)
cpt_aspersor = {
    'T': {'T': 0.1, 'F': 0.9},  # P(A | N=T)
    'F': {'T': 0.5, 'F': 0.5}   # P(A | N=F)
}

# P(L | N)
cpt_lluvia = {
    'T': {'T': 0.8, 'F': 0.2},  # P(L | N=T)
    'F': {'T': 0.2, 'F': 0.8}   # P(L | N=F)
}

# P(PM | A, L)
cpt_pasto_mojado = {
    ('T', 'T'): {'T': 0.99, 'F': 0.01}, # P(PM | A=T, L=T)
    ('T', 'F'): {'T': 0.9, 'F': 0.1},  # P(PM | A=T, L=F)
    ('F', 'T'): {'T': 0.9, 'F': 0.1},  # P(PM | A=F, L=T)
    ('F', 'F'): {'T': 0.0, 'F': 1.0}   # P(PM | A=F, L=F)
}

# Juntamos la red en un solo diccionario para fácil acceso
red_bayesiana = {
    'N': cpt_nublado,
    'A': cpt_aspersor,
    'L': cpt_lluvia,
    'PM': cpt_pasto_mojado
}

print("Red Bayesiana definida con sus CPTs:")
print(f"P(N=T) = {red_bayesiana['N']['T']}")
print(f"P(A=T | N=T) = {red_bayesiana['A']['T']['T']}")
print(f"P(PM=T | A=T, L=F) = {red_bayesiana['PM'][('T', 'F')]['T']}")
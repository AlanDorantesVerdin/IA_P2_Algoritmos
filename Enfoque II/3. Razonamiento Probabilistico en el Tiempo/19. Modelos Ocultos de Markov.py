# Algoritmo 19. Modelos Ocultos de Markov
# Alan Dorantes Verdin

print("\n--- 19. Modelos Ocultos de Markov ---")

# 1. Probabilidades Iniciales (pi)
# Empezamos con 60% Sol, 40% Lluvia
pi = {'Sol': 0.6, 'Lluvia': 0.4}

# 2. Matriz de Transición (A)
# (La misma que en el subtema 16)
transicion_A = {
    'Sol': {'Sol': 0.8, 'Lluvia': 0.2},
    'Lluvia': {'Sol': 0.4, 'Lluvia': 0.6}
}

# 3. Matriz de Emisión (B) - P(Observación | Estado Oculto)
# Observaciones: 'Paraguas', 'Helado'
emision_B = {
    # Dado que el estado es 'Sol'
    'Sol': {'Paraguas': 0.1, 'Helado': 0.9},
    # Dado que el estado es 'Lluvia'
    'Lluvia': {'Paraguas': 0.8, 'Helado': 0.2}
}

hmm_modelo = {
    'pi': pi,
    'A': transicion_A,
    'B': emision_B
}

print("Modelo Oculto de Markov (HMM) definido.")
print(f"P(Empezar con Sol) = {hmm_modelo['pi']['Sol']}")
print(f"P(Lluvia -> Sol) = {hmm_modelo['A']['Lluvia']['Sol']}")
print(f"P(Ver 'Paraguas' | Estado='Lluvia') = {hmm_modelo['B']['Lluvia']['Paraguas']}")
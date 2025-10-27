# Algoritmo 9. Manto de Markov
# Alan Dorantes Verdin

print("\n--- 9. Manto de Markov ---")

def obtener_manto_markov(nodo_objetivo):
    """
    Identifica el Manto de Markov para un nodo en nuestra red
    de Aspersor (definida manualmente).
    """
    # Definimos la estructura de la red manualmente para este ejemplo
    # Padres = {Nodo: [Padres]}
    padres = {
        'N': [],
        'A': ['N'],
        'L': ['N'],
        'PM': ['A', 'L']
    }
    # Hijos = {Nodo: [Hijos]}
    hijos = {
        'N': ['A', 'L'],
        'A': ['PM'],
        'L': ['PM'],
        'PM': []
    }
    
    manto = set() # Usamos un 'set' para evitar duplicados
    
    # 1. Agregar Padres
    for p in padres[nodo_objetivo]:
        manto.add(p)
        
    # 2. Agregar Hijos
    for h in hijos[nodo_objetivo]:
        manto.add(h)
        
    # 3. Agregar "Co-Padres"
    for h in hijos[nodo_objetivo]:
        for copadre in padres[h]:
            if copadre != nodo_objetivo: # No nos agregamos a nosotros mismos
                manto.add(copadre)
                
    return manto

# Ejemplo: ¿Cuál es el manto de Markov de "Aspersor" (A)?
# 1. Padre de A: 'N'
# 2. Hijo de A: 'PM'
# 3. Co-padre (otro padre de 'PM'): 'L'
manto_A = obtener_manto_markov('A')
print(f"Manto de Markov de 'A': {manto_A}")

# Ejemplo: ¿Cuál es el manto de Markov de "Nublado" (N)?
# 1. Padres de N: []
# 2. Hijos de N: 'A', 'L'
# 3. Co-padres (padres de 'A' y 'L'): [] (solo 'N')
manto_N = obtener_manto_markov('N')
print(f"Manto de Markov de 'N': {manto_N}")
# Algoritmo 41. Gramáticas Probabilísticas Lexicalizadas
# Alan Dorantes Verdin

import numpy as np
from collections import defaultdict
import random

# 1. Gramática en Forma Normal de Chomsky (FNC)
# Reglas: A -> B C (No-terminales) o A -> 'palabra' (Terminal)
# (Usamos la misma gramática de 40, pero convertida a FNC)
pcfg_fnc = {
    # A -> 'palabra' (Reglas Léxicas/Terminales)
    "Det": {"el": 0.5, "un": 0.5},
    "N": {"perro": 0.4, "gato": 0.4, "hombre": 0.2},
    "V": {"persigue": 0.5, "come": 0.5},
    
    # A -> B C (Reglas Binarias/Estructurales)
    "S": { ("NP", "VP"): 1.0 },
    "NP": { ("Det", "N"): 0.7 },
    "VP": { ("V", "NP"): 0.6 }
    # (Omitimos NP -> N y VP -> V para mantener FNC simple)
}

def cky_parser(palabras, gramatica):
    """
    Implementación simple del Parser CKY Probabilístico.
    Encuentra la probabilidad del análisis más probable.
    """
    n = len(palabras)
    # Tabla[longitud, inicio, Simbolo] = Probabilidad
    # Usamos diccionarios para simplicidad
    tabla = defaultdict(float)
    
    simbolos_gramatica = list(gramatica.keys())

    # --- 1. Inicialización (Llenar la diagonal) ---
    # Probabilidad de A -> palabra_i
    for i in range(n):
        palabra = palabras[i]
        for simbolo_A in simbolos_gramatica:
            if palabra in gramatica.get(simbolo_A, {}):
                prob = gramatica[simbolo_A][palabra]
                tabla[(1, i, simbolo_A)] = prob

    # --- 2. Llenado Dinámico de la Tabla ---
    # Para longitudes de 2 a n
    for longitud in range(2, n + 1):
        # Para inicios de 0 a n-longitud
        for i in range(n - longitud + 1):
            # Para cada división 'k'
            for k in range(1, longitud):
                
                # Buscar reglas A -> B C (solo claves que sean tuplas de 2 símbolos)
                for simbolo_A in simbolos_gramatica:
                    reglas = gramatica.get(simbolo_A, {})
                    for clave, prob_regla in reglas.items():
                        if not (isinstance(clave, tuple) and len(clave) == 2):
                            continue  # saltar reglas léxicas
                        simbolo_B, simbolo_C = clave
                        
                        prob_B = tabla[(k, i, simbolo_B)]
                        prob_C = tabla[(longitud - k, i + k, simbolo_C)]
                        
                        prob_total = prob_regla * prob_B * prob_C
                        
                        if prob_total > tabla[(longitud, i, simbolo_A)]:
                            tabla[(longitud, i, simbolo_A)] = prob_total

    # 3. Resultado Final
    # La probabilidad está en P(n, 0, 'S')
    prob_final = tabla[(n, 0, "S")]
    return prob_final

# --- Ejecución ---
frase = "el perro persigue un gato"
palabras = frase.split()
prob_analisis = cky_parser(palabras, pcfg_fnc)

print(f"\n--- 41. Parser CKY Probabilístico ---")
print(f"Frase: '{frase}'")
print(f"Probabilidad del análisis más probable: {prob_analisis:.5f}")

frase_mala = "perro el come"
prob_mala = cky_parser(frase_mala.split(), pcfg_fnc)
print(f"\nFrase: '{frase_mala}'")
print(f"Probabilidad del análisis más probable: {prob_mala:.5f} (0.0 = Imposible)")
# Algoritmo 40. Gramáticas Probabilísticas Independientes del Contexto
# Alan Dorantes Verdin

import random

# Definimos una PCFG simple
# S = Oración, NP = Frase Nominal, VP = Frase Verbal, Det = Determinante
# N = Sustantivo, V = Verbo
pcfg_gramatica = {
    "S": [
        (["NP", "VP"], 1.0) # S -> NP VP (Prob 100%)
    ],
    "NP": [
        (["Det", "N"], 0.7), # NP -> Det N (Prob 70%)
        (["N"], 0.3)         # NP -> N (Prob 30%)
    ],
    "VP": [
        (["V", "NP"], 0.6),  # VP -> V NP (Prob 60%)
        (["V"], 0.4)         # VP -> V (Prob 40%)
    ],
    # Reglas Léxicas (Terminales)
    "Det": [
        (["el"], 0.5),
        (["un"], 0.5)
    ],
    "N": [
        (["perro"], 0.4),
        (["gato"], 0.4),
        (["hombre"], 0.2)
    ],
    "V": [
        (["persigue"], 0.5),
        (["come"], 0.5)
    ]
}

def elegir_regla(reglas):
    """Elige una regla basada en sus probabilidades."""
    simbolos_regla = [r[0] for r in reglas]
    probabilidades = [r[1] for r in reglas]
    
    # random.choices devuelve una lista, tomamos el primer (y único) elemento
    return random.choices(simbolos_regla, weights=probabilidades, k=1)[0]

def generar_frase(gramatica, simbolo_actual="S"):
    """
    Genera una frase recursivamente muestreando la PCFG.
    """
    frase = []
    
    # 1. Elegir una regla para el símbolo actual (ej. S -> ['NP', 'VP'])
    regla_elegida = elegir_regla(gramatica[simbolo_actual])
    
    # 2. Iterar sobre los símbolos de la regla elegida
    for simbolo in regla_elegida:
        # Si el símbolo es un No-Terminal (está en la gramática, ej. "NP")
        if simbolo in gramatica:
            # Llamada recursiva
            frase.extend(generar_frase(gramatica, simbolo))
        # Si el símbolo es Terminal (es una palabra, ej. "perro")
        else:
            frase.append(simbolo)
            
    return frase

# --- Ejecución ---
print("\n--- 40. Gramática Probabilística (PCFG) ---")
print("Generando 3 frases aleatorias desde la gramática:")
for i in range(3):
    frase_generada = generar_frase(pcfg_gramatica)
    print(f"  {i+1}. {' '.join(frase_generada)}")
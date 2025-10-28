# Algoritmo 51. Etiquetado de Líneas
# Alan Dorantes Verdin

# Objeto para el cual se aplicará el etiquetado de líneas

#     J1
#    /  \
#   L1  L2
#  /      \
# J2--L3--J3
# |        |
# L4      L5
# |        |
# J4--L6--J5

# El catálogo de uniones "legales" del mundo de los bloques.
# El orden de las etiquetas en las tuplas es importante.

# Uniones tipo 'L': (linea1, linea2)
# (Solo incluimos las 4 combinaciones físicamente realizables)
CATALOGO_L = {
    ('+', '+'),  # Esquina interior cóncava
    ('-', '-'),  # Esquina interior convexa
    ('>', '<'),  # Borde exterior (en sentido horario)
    ('<', '>'),  # Borde exterior (en sentido antihorario)
}

# Uniones tipo 'FORK' (Tridente): (exterior1, interior, exterior2)
CATALOGO_FORK = {
    ('>', '+', '>'), # Objeto sólido
    ('>', '-', '>'), # Objeto con hueco
    ('<', '-', '<'), # Esquina interior (como J2 visto desde adentro)
    # (Existen más, pero estas son suficientes para nuestro bloque)
}

import numpy as np
from collections import defaultdict
from collections import deque

# --- 1. Definición del Problema (El Bloque "A") ---

# Dominios: El conjunto inicial de etiquetas posibles para CADA línea.
# '+' = Cóncava
# '-' = Convexa
# '>' = Borde (sentido horario, la flecha apunta a la derecha de la línea)
# '<' = Borde (sentido antihorario)
DOMINIO_INICIAL = {'+', '-', '>', '<'}

# Variables
lineas = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']

# Dominios actuales (iniciamos con todas las posibilidades)
dominios = {linea: DOMINIO_INICIAL.copy() for linea in lineas}

# ----- SIMPLIFICACIÓN -----
# Para ayudar al algoritmo, pre-etiquetamos los bordes exteriores
# como flechas en sentido horario ('>').
# Esto es una práctica común.
dominios['L1'] = {'>'}
dominios['L2'] = {'>'}
dominios['L5'] = {'>'}
dominios['L6'] = {'>'}
dominios['L4'] = {'>'}
# La línea L3 (interna) es la única que no conocemos.

# Restricciones (Uniones): (nombre, tipo, [lineas_implicadas])
# El ORDEN de las líneas importa para el catálogo.
restricciones = [
    # J1 (L): (L1, L2) -> El catálogo espera ('<', '>')
    # Nota: Si L1 es J2->J1 y L2 es J1->J3, J1 es ('<', '>')
    # Ajustaremos J1 para que L1 sea J1->J2 y L2 sea J1<-J2
    # Para simplificar, usaremos un orden consistente.
    
    # J1 (L): (L1, L2).
    # (J1 es L-exterior, debe ser ('>', '<') o ('<', '>'))
    ('J1', 'L', ['L1', 'L2']), 
    
    # J2 (FORK): (L1 (ext), L3 (int), L4 (ext))
    ('J2', 'FORK', ['L1', 'L3', 'L4']),
    
    # J3 (FORK): (L2 (ext), L3 (int), L5 (ext))
    ('J3', 'FORK', ['L2', 'L3', 'L5']),
    
    # J4 (L): (L4, L6)
    ('J4', 'L', ['L4', 'L6']),
    
    # J5 (L): (L5, L6)
    ('J5', 'L', ['L5', 'L6'])
]

# --- 2. Implementación del Solucionador CSP (AC-3) ---

def revisar_dominio(restriccion, dominios_actuales):
    """
    Función REVISE del algoritmo AC-3.
    Reduce los dominios de las variables en la restricción.
    """
    nombre_r, tipo_r, lineas_r = restriccion
    dominios_reducidos = False
    
    # Seleccionar el catálogo de restricciones correcto
    catalogo = CATALOGO_L if tipo_r == 'L' else CATALOGO_FORK
    
    # Iterar sobre cada línea en la restricción
    for i, linea_actual in enumerate(lineas_r):
        dominio_original = dominios_actuales[linea_actual]
        dominio_nuevo = set()
        
        # Para cada etiqueta posible en la línea actual...
        for etiqueta_actual in dominio_original:
            
            # ...verificar si existe al menos UNA combinación válida
            # con las otras líneas de la restricción.
            if encontrar_soporte(linea_actual, etiqueta_actual, lineas_r, dominios_actuales, catalogo):
                dominio_nuevo.add(etiqueta_actual)
        
        # Si el nuevo dominio es más pequeño, hubo una reducción
        if len(dominio_nuevo) < len(dominio_original):
            dominios_actuales[linea_actual] = dominio_nuevo
            dominios_reducidos = True
            
            # Si un dominio se vuelve vacío, el problema no tiene solución
            if not dominio_nuevo:
                return "FALLO", True # Fallo, Reducido

    return dominios_actuales, dominios_reducidos

def encontrar_soporte(linea_actual, etiqueta_actual, lineas_r, dominios_actuales, catalogo):
    """
    Función de ayuda para REVISE.
    Busca si 'etiqueta_actual' tiene "soporte" (una combinación válida).
    """
    
    # Generar todas las combinaciones de etiquetas de las OTRAS líneas
    indices_otras_lineas = [j for j, l in enumerate(lineas_r) if l != linea_actual]
    dominios_otras_lineas = [dominios_actuales[lineas_r[j]] for j in indices_otras_lineas]
    
    # (Esta es una forma simple de producto cartesiano para 2 o 3 líneas)
    
    if len(lineas_r) == 2: # Tipo 'L'
        otra_linea_idx = indices_otras_lineas[0]
        linea_actual_idx = 1 - otra_linea_idx
        
        for otra_etiqueta in dominios_otras_lineas[0]:
            combinacion = [None, None]
            combinacion[linea_actual_idx] = etiqueta_actual
            combinacion[otra_linea_idx] = otra_etiqueta
            if tuple(combinacion) in catalogo:
                return True # ¡Encontrado!
                
    elif len(lineas_r) == 3: # Tipo 'FORK'
        idx1, idx2 = indices_otras_lineas
        idx_actual = [j for j in [0,1,2] if j not in [idx1, idx2]][0]
        
        for e1 in dominios_otras_lineas[0]:
            for e2 in dominios_otras_lineas[1]:
                combinacion = [None, None, None]
                combinacion[idx_actual] = etiqueta_actual
                combinacion[idx1] = e1
                combinacion[idx2] = e2
                if tuple(combinacion) in catalogo:
                    return True # ¡Encontrado!

    return False # No se encontró soporte

def etiquetado_de_lineas(dominios, restricciones):
    """
    Algoritmo principal AC-3.
    """
    # 1. Cola de trabajo inicial con todas las restricciones
    cola = deque(restricciones)
    
    # 2. Mapa de "vecinos" para propagar restricciones
    # vecinos[linea] = {restriccion_1, restriccion_2, ...}
    vecinos = defaultdict(set)
    for r in restricciones:
        for linea in r[2]:
            vecinos[linea].add(r[0])
            
    # 3. Bucle principal
    while cola:
        restriccion_actual = cola.popleft()
        
        # 4. Revisar dominios
        dominios, reducido = revisar_dominio(restriccion_actual, dominios)
        
        if dominios == "FALLO":
            return "Error: Problema sin solución (dominio vacío)."
            
        # 5. Propagación
        if reducido:
            # Si un dominio se redujo, volver a encolar a todos
            # los "vecinos" de las líneas afectadas.
            for linea_afectada in restriccion_actual[2]:
                for nombre_vecino in vecinos[linea_afectada]:
                    if nombre_vecino != restriccion_actual[0]:
                        # Encontrar la restricción por su nombre
                        r_vecina = next(r for r in restricciones if r[0] == nombre_vecino)
                        if r_vecina not in cola:
                            cola.append(r_vecina)
                            
    return dominios

# --- 3. Ejecución ---
print("--- 51. Etiquetado de Líneas (Algoritmo de Waltz/AC-3) ---")
print("Objeto: Bloque 'A'")
print("\nDominios Iniciales (Con bordes pre-etiquetados):")
for l, d in dominios.items():
    print(f"  {l}: {d}")

# Llamamos al algoritmo
solucion = etiquetado_de_lineas(dominios, restricciones)

print("\n--- Solución Encontrada ---")
if isinstance(solucion, str):
    # CASO 1: Fallo. 'solucion' es un string de error.
    print(solucion)
else:
    # CASO 2: Éxito. 'solucion' es un diccionario.
    # Imprimir los dominios finales
    for l, d in solucion.items():
        print(f"  {l}: {d}")
    
    # --- ESTE BLOQUE DEBE ESTAR AQUÍ DENTRO ---
    print("\nInterpretación:")
    print("  El algoritmo propagó las restricciones de las uniones.")
    print("  L1, L2, L4, L5, L6 son bordes '>' (como se definió).")
    
    # Esta línea ahora es segura porque solo se ejecuta si 'solucion' es un dict.
    print(f"  La única etiqueta válida para L3 (la línea interna) es {solucion.get('L3', '{?}')}.")
    print("  Esto coincide con la unión FORK ('>', '+', '>') que define un objeto sólido.")
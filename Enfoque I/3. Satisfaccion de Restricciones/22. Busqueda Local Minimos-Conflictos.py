# Algoritmo 22. Búsqueda Local: Mínimos Conflictos
# Alan Dorantes Verdin

import random

# 1. Variables (Estados de Australia)
variables_csp = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

# 2. Dominios (Valores posibles para cada variable)
colores = {'Rojo', 'Verde', 'Azul'}
dominios_csp = {var: colores.copy() for var in variables_csp}

# 3. Restricciones (Qué estados son vecinos)
# (WA, NT), (WA, SA), (NT, SA), (NT, Q), (SA, Q), 
# (SA, NSW), (SA, V), (Q, NSW), (NSW, V)
# (T no tiene vecinos en esta lista)
restricciones_csp = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['Q', 'SA', 'V'],
    'V': ['SA', 'NSW'],
    'T': []
}

def get_conflictos(variable, valor, asignacion_actual, restricciones):
    """Cuenta cuántos vecinos de 'variable' entran en conflicto con 'valor'."""
    conteo = 0
    for vecino in restricciones[variable]:
        if asignacion_actual[vecino] == valor:
            conteo += 1
    return conteo

def min_conflictos(variables, dominios, restricciones, max_pasos=1000):
    """
    Intenta resolver el CSP usando Mínimos-Conflictos.
    """
    print(f"Iniciando Búsqueda Local (Mínimos-Conflictos) con {max_pasos} pasos...")
    
    # 1. Crear una asignación completa aleatoria
    asignacion = {var: random.choice(list(dominios[var])) for var in variables}
    print(f"Asignación inicial (aleatoria): {asignacion}")

    for i in range(max_pasos):
        
        # 2. Encontrar todas las variables en conflicto
        variables_en_conflicto = []
        for var in variables:
            # Si esta variable tiene algún conflicto, añadirla a la lista
            if get_conflictos(var, asignacion[var], asignacion, restricciones) > 0:
                variables_en_conflicto.append(var)
        
        # 3. Si no hay conflictos, ¡éxito!
        if not variables_en_conflicto:
            print(f"\n¡Solución encontrada en el paso {i}!")
            return asignacion
            
        # 4. Elegir una variable en conflicto al azar
        var_conflicto = random.choice(variables_en_conflicto)
        
        # 5. Encontrar el valor que minimiza los conflictos para esta variable
        mejor_valor = asignacion[var_conflicto]
        min_conflictos = get_conflictos(var_conflicto, mejor_valor, asignacion, restricciones)

        for valor in dominios[var_conflicto]:
            conteo = get_conflictos(var_conflicto, valor, asignacion, restricciones)
            if conteo < min_conflictos:
                min_conflictos = conteo
                mejor_valor = valor
                
        # 6. Asignar el nuevo mejor valor (incluso si no es 0 conflictos)
        if asignacion[var_conflicto] != mejor_valor:
            # print(f"Paso {i}: Cambiando {var_conflicto} a {mejor_valor} (Conflictos: {min_conflictos})")
            asignacion[var_conflicto] = mejor_valor

    print("\nNo se encontró solución (se alcanzó el límite de pasos).")
    return None

# Ejemplo de uso
print("--- 22. Búsqueda Local: Mínimos-Conflictos ---")
# (Puede fallar a veces, es estocástico)
solucion_mc = min_conflictos(variables_csp, dominios_csp, restricciones_csp)
if solucion_mc:
    print(f"Solución encontrada: {solucion_mc}\n")
else:
    print("Intento fallido (prueba de nuevo).\n")
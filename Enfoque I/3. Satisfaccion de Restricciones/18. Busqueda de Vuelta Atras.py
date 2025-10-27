# Algoritmo 18. Búsqueda de Vuelta Atrás (Backtracking)
# Alan Dorantes Verdin

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

def es_consistente(variable, valor, asignacion, restricciones):
    """
    Verifica si asignar 'valor' a 'variable' es consistente
    con la 'asignacion' actual.
    """
    for vecino in restricciones.get(variable, []):
        if vecino in asignacion and asignacion[vecino] == valor:
            # Conflicto: El vecino ya tiene este color
            return False
    return True

def seleccionar_variable_no_asignada(variables, asignacion):
    """Encuentra la primera variable que aún no tiene un valor."""
    for var in variables:
        if var not in asignacion:
            return var
    return None

def backtracking_search(variables, dominios, restricciones):
    """
    Función principal que inicia la búsqueda recursiva.
    """
    print("Iniciando Búsqueda de Vuelta Atrás (Backtracking)...")
    
    # Llama a la función recursiva
    return backtrack_recursivo({}, variables, dominios, restricciones)

def backtrack_recursivo(asignacion, variables, dominios, restricciones):
    """
    El núcleo recursivo de Backtracking.
    """
    
    # 1. Caso Base: Si la asignación está completa, lo logramos.
    if len(asignacion) == len(variables):
        return asignacion

    # 2. Seleccionar una variable para asignarle valor
    var = seleccionar_variable_no_asignada(variables, asignacion)
    
    # 3. Probar cada valor en el dominio de la variable
    for valor in dominios[var]:
        
        # 4. Verificar si el valor es consistente
        if es_consistente(var, valor, asignacion, restricciones):
            
            # 5. Asignar (Probar)
            asignacion[var] = valor
            # print(f"Probando: {var} = {valor}") # (Descomentar para traza)
            
            # 6. Llamada recursiva (profundizar)
            resultado = backtrack_recursivo(asignacion, variables, dominios, restricciones)
            
            if resultado is not None:
                # Si la recursión tuvo éxito, propagar el éxito
                return resultado
            
            # 7. Fallo (Backtrack): Deshacer la asignación
            # print(f"Fallo (Backtrack): {var} = {valor}") # (Descomentar para traza)
            del asignacion[var]
            
    # 8. Si probamos todos los valores y ninguno funcionó, fallamos.
    return None

# Ejemplo de uso
print("\n--- 18. Búsqueda de Vuelta Atrás (Backtracking) ---")
solucion_backtrack = backtracking_search(variables_csp, dominios_csp, restricciones_csp)
if solucion_backtrack:
    print(f"Solución encontrada: {solucion_backtrack}\n")
else:
    print("No se encontró solución.\n")
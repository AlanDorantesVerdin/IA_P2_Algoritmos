# Algoritmo 23. Acondicionamiento del Corte
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

# Usaremos la función de backtracking simple (del Subtema 18)
# como nuestro "solucionador de árboles"
def es_consistente_simple(variable, valor, asignacion, restricciones):
    for vecino in restricciones.get(variable, []):
        if vecino in asignacion and asignacion[vecino] == valor:
            return False
    return True

def backtrack_simple_para_cutset(asignacion_inicial, variables_a_resolver, dominios, restricciones):
    """
    Un backtracking simple que resuelve las 'variables_a_resolver'
    dada una 'asignacion_inicial' (el cutset).
    """
    
    # Copiamos la asignación inicial para trabajar sobre ella
    asignacion = asignacion_inicial.copy()
    
    def recursivo(vars_pendientes):
        if not vars_pendientes:
            return asignacion # Éxito

        var = vars_pendientes[0]
        resto_vars = vars_pendientes[1:]
        
        for valor in dominios[var]:
            if es_consistente_simple(var, valor, asignacion, restricciones):
                asignacion[var] = valor
                
                resultado = recursivo(resto_vars)
                if resultado:
                    return resultado
                
                del asignacion[var] # Backtrack
        return None # Fallo

    return recursivo(variables_a_resolver)


def cutset_conditioning(variables, dominios, restricciones):
    """
    Resuelve el CSP usando Acondicionamiento del Corte.
    """
    
    # 1. Identificar el Cutset (hardcodeado por simplicidad)
    # 'SA' rompe todos los ciclos en el mapa de Australia.
    # 'T' no tiene restricciones, así que lo ponemos en 'resto'.
    variables_cutset = ['SA']
    variables_resto = [v for v in variables if v not in variables_cutset]
    
    print(f"Cutset seleccionado: {variables_cutset}")
    print(f"Variables restantes (árbol): {variables_resto}")

    # 2. Iterar (Backtrack) sobre los valores del Cutset
    # (Usamos una función recursiva simple para manejar cutsets > 1 variable)
    
    def iterar_cutset(asignacion_cutset, vars_cutset_pendientes):
        
        # 3. Si el cutset está completo...
        if not vars_cutset_pendientes:
            # 4. ...resolver el "árbol" restante
            print(f"Probando cutset: {asignacion_cutset}") # (Traza)
            solucion_arbol = backtrack_simple_para_cutset(
                asignacion_cutset, variables_resto, dominios, restricciones
            )
            return solucion_arbol # Devuelve la solución o None

        var_cutset = vars_cutset_pendientes[0]
        resto_cutset = vars_cutset_pendientes[1:]

        for valor in dominios[var_cutset]:
            asignacion_cutset[var_cutset] = valor
            
            resultado = iterar_cutset(asignacion_cutset, resto_cutset)
            if resultado:
                return resultado # ¡Éxito!
            
            del asignacion_cutset[var_cutset] # Backtrack del cutset
            
        return None # Fallo en esta rama del cutset

    # Iniciar la iteración del cutset
    return iterar_cutset({}, variables_cutset)

# --- Ejemplo de uso ---
print("\n--- 23. Acondicionamiento del Corte (Cutset Conditioning) ---")
solucion_cutset = cutset_conditioning(variables_csp, dominios_csp, restricciones_csp)
if solucion_cutset:
    print(f"Solución encontrada: {solucion_cutset}\n")
else:
    print("No se encontró solución.\n")
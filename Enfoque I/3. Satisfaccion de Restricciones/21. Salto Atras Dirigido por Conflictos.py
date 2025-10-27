# Algoritmo 21. Salto Atrás Dirigido por Conflictos (Conflict-Driven Backtracking)
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

# --- Funciones de ayuda para CBJ ---
def seleccionar_variable_no_asignada(variables, asignacion):
    """Encuentra la primera variable que aún no tiene un valor."""
    for var in variables:
        if var not in asignacion:
            return var
    return None

def es_consistente_y_devuelve_conflicto(var, valor, asignacion, restricciones):
    """
    Verifica si la asignación es consistente.
    Si no lo es, devuelve (False, variable_en_conflicto).
    """
    for vecino in restricciones[var]:
        if vecino in asignacion and asignacion[vecino] == valor:
            return (False, vecino) # Conflicto con 'vecino'
    return (True, None) # Es consistente

def cbj_search(variables, dominios, restricciones):
    """
    Función principal que inicia la búsqueda CBJ.
    """
    print("Iniciando Salto Atrás Dirigido por Conflictos (CBJ)...")
    
    # Llama a la función recursiva
    (solucion, _) = cbj_recursivo({}, variables, dominios, restricciones)
    return solucion

def cbj_recursivo(asignacion, variables, dominios, restricciones):
    """
    El núcleo recursivo de CBJ.
    Retorna: (solucion, conflict_set)
    """
    
    # 1. Caso Base: Éxito
    if len(asignacion) == len(variables):
        return (asignacion, set())

    var = seleccionar_variable_no_asignada(variables, asignacion)
    
    # Conflict set de esta variable (los conflictos que sus hijos le reporten)
    conflict_set_agregado = set()
    
    for valor in dominios[var]:
        
        # 2. Verificar consistencia con el PASADO
        (consistente, var_conflicto_pasado) = es_consistente_y_devuelve_conflicto(
            var, valor, asignacion, restricciones
        )
        
        if consistente:
            asignacion[var] = valor
            
            # 3. Llamada recursiva (FUTURO)
            (resultado, conflict_set_hijo) = cbj_recursivo(
                asignacion, variables, dominios, restricciones
            )
            
            # 4. Éxito
            if resultado is not None:
                return (resultado, set())
            
            # 5. Fallo en el futuro: El hijo (ej. NT) falló.
            #    'conflict_set_hijo' dice por qué (ej. {'WA'}).
            del asignacion[var]
            
            # 6. ¿El conflicto es conmigo (var) o con alguien antes que yo?
            if var in conflict_set_hijo:
                # El conflicto SÍ involucra mi asignación actual.
                # Lo removemos y agregamos el resto al set agregado.
                conflict_set_agregado.update(conflict_set_hijo - {var})
            else:
                # ¡EL SALTO (JUMP)!
                # El conflicto (ej. {'WA'}) no tiene nada que ver conmigo ('SA').
                # No pruebo más valores para 'SA'. Fallo inmediatamente
                # y paso el 'conflict_set_hijo' intacto hacia arriba.
                return (None, conflict_set_hijo)
                
        else:
            # 2b. El valor falló contra el PASADO (ej. 'WA')
            conflict_set_agregado.add(var_conflicto_pasado)
            
    # 7. Fallo total: Probé todos mis valores y fallaron.
    # Devuelvo todos los conflictos que encontré (pasados + futuros).
    return (None, conflict_set_agregado)

# --- Ejemplo de uso ---
print("\n--- 21. Salto Atrás Dirigido por Conflictos (CBJ) ---")
solucion_cbj = cbj_search(variables_csp, dominios_csp, restricciones_csp)
if solucion_cbj:
    print(f"Solución encontrada: {solucion_cbj}\n")
else:
    print("No se encontró solución.\n")
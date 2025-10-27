# Algoritmo 19. Comprobación Hacia Delante (Forward Checking)
# Alan Dorantes Verdin

import copy

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

def seleccionar_variable_no_asignada(variables, asignacion):
    """
    Selecciona la siguiente variable no asignada.
    Estrategia simple: toma la primera variable no asignada.
    """
    for var in variables:
        if var not in asignacion:
            return var
    return None

def forward_checking(variables, dominios, restricciones):
    """
    Inicia la búsqueda con Forward Checking.
    """
    print("Iniciando Búsqueda con Comprobación Hacia Delante (FC)...")
    # Necesitamos pasar copias de los dominios en la recursión
    return fc_recursivo({}, variables, copy.deepcopy(dominios), restricciones)

def fc_recursivo(asignacion, variables, dominios, restricciones):
    """
    Núcleo recursivo de Forward Checking.
    """
    if len(asignacion) == len(variables):
        return asignacion

    var = seleccionar_variable_no_asignada(variables, asignacion)
    
    for valor in list(dominios[var]): # Iteramos sobre una copia del dominio
        
        # 1. Asignar (Probar)
        asignacion[var] = valor
        # print(f"Probando: {var} = {valor}") # (Traza)
        
        # 2. 'dominios_pruned' guardará los dominios afectados
        dominios_pruned = copy.deepcopy(dominios)
        
        # 3. Comprobación Hacia Delante (Forward Check)
        fallo_fc = False
        for vecino in restricciones[var]:
            if vecino not in asignacion:
                # Si el vecino aún no está asignado...
                if valor in dominios_pruned[vecino]:
                    # ...eliminamos el valor de su dominio
                    dominios_pruned[vecino].remove(valor)
                    
                    if not dominios_pruned[vecino]:
                        # ¡Fallo! Este vecino se quedó sin valores.
                        fallo_fc = True
                        break # Dejar de revisar vecinos
        
        # 4. Si la comprobación hacia delante NO falló...
        if not fallo_fc:
            # 5. ...continuamos con la recursión
            resultado = fc_recursivo(asignacion, variables, dominios_pruned, restricciones)
            if resultado is not None:
                return resultado
        
        # 6. Fallo (Backtrack): Deshacer la asignación
        # (No necesitamos deshacer los dominios podados, 
        # porque en la siguiente iteración del bucle 'for valor...'
        # usaremos la 'dominios' original (sin podar) de esta llamada).
        del asignacion[var]
        # print(f"Fallo (Backtrack): {var} = {valor}") # (Traza)
            
    return None

# Ejemplo de uso
print("\n--- 19. Comprobación Hacia Delante (Forward Checking) ---")
solucion_fc = forward_checking(variables_csp, dominios_csp, restricciones_csp)
if solucion_fc:
    print(f"Solución encontrada: {solucion_fc}\n")
else:
    print("No se encontró solución.\n")
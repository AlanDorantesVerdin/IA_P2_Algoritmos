# Algoritmo 20. Propagación de Restricciones (Constraint Propagation)
# Alan Dorantes Verdin

import copy
from collections import deque

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

def revise(xi, xj, dominios, restricciones):
    """
    Función auxiliar para AC-3.
    Revisa el arco (Xi, Xj).
    Elimina valores del dominio de Xi si no tienen "soporte" en Xj.
    """
    revised = False
    
    # Restricción: color de Xi debe ser != color de Xj
    
    # Iteramos sobre una copia del dominio de Xi
    for valor_x in list(dominios[xi]):
        
        # ¿Existe algún valor 'valor_y' en Xj que sea compatible?
        tiene_soporte = False
        for valor_y in dominios[xj]:
            if valor_x != valor_y: # Esta es la restricción
                tiene_soporte = True
                break
        
        # Si 'valor_x' no tiene soporte (ningún valor_y es compatible)
        if not tiene_soporte:
            dominios[xi].remove(valor_x)
            revised = True # Marcamos que hicimos un cambio
            
    return revised

def ac3(variables, dominios_originales, restricciones):
    """
    Algoritmo AC-3 para hacer el CSP arco-consistente.
    """
    print("\nIniciando Propagación de Restricciones (AC-3)...")
    
    # Hacemos una copia profunda para no modificar los dominios originales
    dominios = copy.deepcopy(dominios_originales)
    
    # 1. Crear la cola de arcos (bidireccional)
    cola_arcos = deque()
    for var in variables:
        for vecino in restricciones[var]:
            cola_arcos.append((var, vecino))
            
    # 2. Procesar la cola
    while cola_arcos:
        (xi, xj) = cola_arcos.popleft()
        
        # 3. Revisar el arco
        if revise(xi, xj, dominios, restricciones):
            
            # 4. Si el dominio de Xi se quedó vacío, el CSP es irresoluble
            if not dominios[xi]:
                print("Fallo: Dominio de", xi, "quedó vacío.")
                return None # No hay solución
                
            # 5. Si 'revise' eliminó algo, debemos re-agregar los arcos
            #    de los vecinos de Xi (excepto Xj) apuntando a Xi.
            for xk in restricciones[xi]:
                if xk != xj:
                    cola_arcos.append((xk, xi))
                    
    print("AC-3 completado. Dominios podados:")
    return dominios

# --- Ejemplo de uso ---
print("\n--- 20. Propagación de Restricciones ---")
# Añadamos una restricción extra para que AC-3 haga algo:
dominios_con_restriccion = copy.deepcopy(dominios_csp)
dominios_con_restriccion['WA'] = {'Rojo'} # Forzamos a WA a ser Rojo
dominios_con_restriccion['NT'] = {'Rojo', 'Verde'}

print(f"Dominios iniciales (restringidos):")
print(f"  WA: {dominios_con_restriccion['WA']}")
print(f"  NT: {dominios_con_restriccion['NT']}")
print(f"  SA: {dominios_con_restriccion['SA']}")

# Ejecutamos AC-3
dominios_podados = ac3(variables_csp, dominios_con_restriccion, restricciones_csp)

if dominios_podados:
    print("Dominios después de AC-3:")
    print(f"  WA (fijo): {dominios_podados['WA']}")
    print(f"  NT (vecino de WA): {dominios_podados['NT']}") # Debería perder 'Rojo'
    print(f"  SA (vecino de WA): {dominios_podados['SA']}\n") # Debería perder 'Rojo'
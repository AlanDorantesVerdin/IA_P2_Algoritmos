# Algoritmo 17. Problemas de Satisfacción de Restricciones (CSP)
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

# Ejemplo de impresión de la configuración del CSP
print("\n--- 17. Problema de Satisfacción de Restricciones (CSP) ---")
print("Variables, Dominios y Restricciones del problema de coloreo de mapas de Australia:")
print(f"Variables: {variables_csp}")
print(f"Dominios: {dominios_csp['WA']}")
print(f"Restricción (vecinos de 'SA'): {restricciones_csp['SA']}\n")
# Algoritmo 32. Teoría de Juegos - Equilibrios y Mecanismos
# Alan Dorantes Verdin

print("\n--- 32. Teoría de Juegos (Equilibrio de Nash) ---")

# Matriz de Pagos (Utilidad de P1, Utilidad de P2)
# Usaremos pagos positivos (más es mejor)
# P1 (Arriba/Abajo), P2 (Izq/Der)
#
# P2: Izq      P2: Der
# P1:Arriba  (A, a)     (B, b)
# P1:Abajo   (C, c)     (D, d)

# Ejemplo: Dilema del Prisionero (Pagos = -(años de cárcel))
# P2: Confesar   P2: Callar
# P1:Conf.   (-5, -5)      (0, -10)
# P1:Callar  (-10, 0)      (-1, -1)
pagos = {
    'Arriba': { 'Izq': (-5, -5), 'Der': (0, -10) },
    'Abajo':  { 'Izq': (-10, 0), 'Der': (-1, -1) }
}

print("Buscando Equilibrio de Nash en Estrategias Puras...")

# 1. Encontrar la mejor respuesta de P1 para cada acción de P2
mejor_resp_p1 = {}
# Asume P2 juega 'Izq'
pago_arriba = pagos['Arriba']['Izq'][0] # P1
pago_abajo = pagos['Abajo']['Izq'][0]  # P1
mejor_resp_p1['Izq'] = 'Arriba' if pago_arriba >= pago_abajo else 'Abajo'

# Asume P2 juega 'Der'
pago_arriba = pagos['Arriba']['Der'][0]
pago_abajo = pagos['Abajo']['Der'][0]
mejor_resp_p1['Der'] = 'Arriba' if pago_arriba >= pago_abajo else 'Abajo'

# 2. Encontrar la mejor respuesta de P2 para cada acción de P1
mejor_resp_p2 = {}
# Asume P1 juega 'Arriba'
pago_izq = pagos['Arriba']['Izq'][1] # P2
pago_der = pagos['Arriba']['Der'][1] # P2
mejor_resp_p2['Arriba'] = 'Izq' if pago_izq >= pago_der else 'Der'

# Asume P1 juega 'Abajo'
pago_izq = pagos['Abajo']['Izq'][1]
pago_der = pagos['Abajo']['Der'][1]
mejor_resp_p2['Abajo'] = 'Izq' if pago_izq >= pago_der else 'Der'

print(f"Mejor respuesta de P1 (dado P2): {mejor_resp_p1}")
print(f"Mejor respuesta de P2 (dado P1): {mejor_resp_p2}")

# 3. Encontrar el equilibrio (donde las respuestas son mutuas)
equilibrios = []
for accion_p1 in ['Arriba', 'Abajo']:
    for accion_p2 in ['Izq', 'Der']:
        
        # ¿Es 'accion_p1' la mejor respuesta a 'accion_p2'?
        es_mejor_p1 = (mejor_resp_p1[accion_p2] == accion_p1)
        # ¿Es 'accion_p2' la mejor respuesta a 'accion_p1'?
        es_mejor_p2 = (mejor_resp_p2[accion_p1] == accion_p2)
        
        if es_mejor_p1 and es_mejor_p2:
            equilibrios.append((accion_p1, accion_p2))

if equilibrios:
    print(f"\nEquilibrios de Nash encontrados: {equilibrios}")
    for eq in equilibrios:
        print(f"  Pago: {pagos[eq[0]][eq[1]]}")
else:
    print("\nNo se encontró Equilibrio de Nash en estrategias puras.")
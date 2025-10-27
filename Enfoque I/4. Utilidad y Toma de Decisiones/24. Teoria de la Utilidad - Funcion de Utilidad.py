# Algoritmo 24. Teoría de la Utilidad - Función de Utilidad
# Alan Dorantes Verdin

import math

def utilidad_con_aversion(dinero):
    """
    Función de utilidad cóncava (logarítmica).
    Refleja que cada dólar adicional vale menos que el anterior.
    (Sumamos 1 para evitar log(0))
    """
    if dinero < 0:
        return -math.log(abs(dinero) + 1) # Perder dinero duele
    return math.log(dinero + 1)

print("\n--- 24. Función de Utilidad (Aversión al Riesgo) ---")
dinero_1 = 1000
dinero_2 = 1000000

utilidad_1 = utilidad_con_aversion(dinero_1)
utilidad_2 = utilidad_con_aversion(dinero_2)
doble_utilidad_1 = 2 * utilidad_1

print(f"Utilidad de ${dinero_1}: {utilidad_1:.2f}")
print(f"Utilidad de ${dinero_2}: {utilidad_2:.2f}")
# Comparamos si 1 millón es 1000 veces mejor
print(f"1000 veces la utilidad de $1000: {1000 * utilidad_1:.2f} (Mucho mayor)")
# Comparamos si 1 millón da el doble de utilidad que 1000
print(f"El doble de utilidad de $1000: {doble_utilidad_1:.2f} (Mucho menor que U($1M))")
print("Esto muestra que 1 millón NO es 1000 veces 'mejor' que 1000.\n")
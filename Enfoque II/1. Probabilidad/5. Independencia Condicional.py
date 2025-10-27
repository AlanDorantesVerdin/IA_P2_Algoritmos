# Algoritmo 5. Independencia Condicional
# Alan Dorantes Verdin

print("\n--- 5. Independencia Condicional ---")

def verificar_independencia_condicional(P_A_dado_B_C, P_A_dado_C):
    """
    Verifica si A es condicionalmente independiente de B dado C,
    comparando P(A|B,C) y P(A|C).
    """
    # Comparamos si las dos probabilidades son (casi) iguales
    if abs(P_A_dado_B_C - P_A_dado_C) < 0.0001:
        return True
    else:
        return False

# Ejemplo:
# A = "El suelo está mojado"
# B = "El aspersor estaba encendido"
# C = "Llovió"

# Si sabemos que llovió (C=True), la probabilidad de que el suelo esté 
# mojado (A) es alta.
# Saber si el aspersor estaba encendido (B) no nos da mucha más 
# información, porque la lluvia ya explica el suelo mojado.

# Asignamos probabilidades hipotéticas para la demostración:
P_SueloMojado_dado_Aspersor_Lluvia = 0.95
P_SueloMojado_dado_Lluvia = 0.95 # Igual que arriba, indicando independencia

es_independiente = verificar_independencia_condicional(
    P_SueloMojado_dado_Aspersor_Lluvia,
    P_SueloMojado_dado_Lluvia
)

print(f"¿Es 'Suelo Mojado' independiente de 'Aspersor' dado que 'Llovió'? {es_independiente}")
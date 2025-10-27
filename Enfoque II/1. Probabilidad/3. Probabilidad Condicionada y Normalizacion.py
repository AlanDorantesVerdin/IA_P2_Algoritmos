# Algoritmo 3. Probabilidad Condicionada y Normalización
# Alan Dorantes Verdin

def probabilidad_condicionada(P_A_y_B, P_B):
    """
    Calcula la probabilidad condicionada P(A|B) usando la fórmula:
    P(A|B) = P(A y B) / P(B)
    """
    if P_B == 0:
        return 0  # No se puede condicionar sobre un evento imposible
    
    return P_A_y_B / P_B

# --- Ejemplo de Probabilidad Condicionada ---
# Datos:
# P(Lluvia y Nublado) = 0.2
# P(Nublado) = 0.4

P_lluvia_y_nublado = 0.2
P_nublado = 0.4

print("\n--- 3. Normalización de Probabilidades Condicionadas ---")

P_lluvia_dado_nublado = probabilidad_condicionada(P_lluvia_y_nublado, P_nublado)
print(f"P(Lluvia | Nublado) = {P_lluvia_dado_nublado}")


# --- Ejemplo de Normalización ---
# Supongamos que P(Nublado) = 0.4, y sabemos:
# P(Lluvia | Nublado) = 0.5  (Calculado arriba)
# P(No Lluvia | Nublado) = 0.5 (Esto es un supuesto para el ejemplo)

# La normalización verifica que P(Lluvia|Nublado) + P(No Lluvia|Nublado) = 1
prob_A_dado_B = 0.5
prob_no_A_dado_B = 0.5

suma_normalizada = prob_A_dado_B + prob_no_A_dado_B


print(f"\nSuma de probabilidades condicionadas (normalización): {suma_normalizada}")
if suma_normalizada == 1.0:
    print("El conjunto de probabilidades está normalizado.")
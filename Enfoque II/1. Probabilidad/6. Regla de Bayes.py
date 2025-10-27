# Algoritmo 6. Regla de Bayes
# Alan Dorantes Verdin

print("\n--- 6. Regla de Bayes ---")

def regla_de_bayes(P_A, P_B_dado_A, P_B):
    """
    Calcula la probabilidad posterior P(A|B) usando la Regla de Bayes.
    
    P_A: Probabilidad a priori de A.
    P_B_dado_A: Probabilidad de B dado A (Verosimilitud).
    P_B: Probabilidad total de B (Evidencia).
    """
    if P_B == 0:
        return 0
        
    numerador = P_B_dado_A * P_A
    P_A_dado_B = numerador / P_B
    return P_A_dado_B

# Ejemplo: Prueba de diagnóstico médico
# A = "El paciente tiene la enfermedad"
# B = "El paciente da positivo en la prueba"

# 1. Probabilidad a priori P(A)
# Prevalencia de la enfermedad en la población
P_A = 0.01  # 1% de la población tiene la enfermedad

# 2. Verosimilitud P(B|A)
# Sensibilidad de la prueba: Si tienes la enfermedad, ¿qué prob. hay de dar positivo?
P_B_dado_A = 0.99  # 99% (tasa de verdaderos positivos)

# 3. Probabilidad total de la evidencia P(B)
# ¿Cuál es la probabilidad de que alguien (cualquiera) dé positivo?
# P(B) = P(B|A) * P(A) + P(B|no A) * P(no A)

# Necesitamos P(B|no A), la tasa de falsos positivos
# P(no A) = 1 - P(A) = 0.99
# P(B|no A) = 0.05  # 5% de la gente sana da positivo (falso positivo)

P_no_A = 1 - P_A
P_B_dado_no_A = 0.05

P_B = (P_B_dado_A * P_A) + (P_B_dado_no_A * P_no_A)
# P_B = (0.99 * 0.01) + (0.05 * 0.99) = 0.0099 + 0.0495 = 0.0594

print(f"Probabilidad total de dar positivo P(B): {P_B:.4f}")

# 4. Calcular P(A|B)
# Si un paciente da positivo (B), ¿cuál es la probabilidad de que realmente 
# tenga la enfermedad (A)?
P_A_dado_B = regla_de_bayes(P_A, P_B_dado_A, P_B)

print(f"Probabilidad a priori de tener la enfermedad P(A): {P_A}")
print(f"Probabilidad posterior (dado un test positivo) P(A|B): {P_A_dado_B:.4f}")
# Nota: Aunque la prueba es precisa (99%), si das positivo, solo tienes 
# un 16.6% de probabilidad de tener la enfermedad.
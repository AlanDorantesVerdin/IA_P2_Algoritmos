# Algoritmo 2. Probabilidad a Priori
# Alan Dorantes Verdin

def calcular_probabilidad_a_priori(eventos_favorables, total_eventos):
    """
    Calcula la probabilidad a priori de un evento.
    P(A) = (Número de resultados favorables a A) / (Total de resultados posibles)
    """
    
    # Asegurarse de no dividir por cero
    if total_eventos == 0:
        return 0
        
    # Cálculo de la probabilidad
    probabilidad = eventos_favorables / total_eventos
    return probabilidad

# Ejemplo: Una bolsa con 10 canicas (3 rojas, 7 azules)
# ¿Cuál es la probabilidad a priori de sacar una canica roja?
canicas_rojas = 3
total_canicas = 10

prob_roja = calcular_probabilidad_a_priori(canicas_rojas, total_canicas)

print("\n--- 2. Probabilidad a Priori ---")
print(f"Total de canicas: {total_canicas}")
print(f"Canicas rojas: {canicas_rojas}")
print(f"Probabilidad a priori de sacar una roja: {prob_roja}")
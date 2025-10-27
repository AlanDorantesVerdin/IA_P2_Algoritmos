# Algoritmo 1. Incertidumbre
# Alan Dorantes Verdin

import random

def demostrar_incertidumbre():
    """
    Simula un evento incierto: lanzar un dado de 6 caras.
    El resultado no se conoce antes de ejecutar la función.
    """
    # Lista de posibles resultados
    posibles_resultados = [1, 2, 3, 4, 5, 6]
    
    # La función 'choice' selecciona un elemento al azar
    resultado = random.choice(posibles_resultados)
    
    print("\n--- 1. Incertidumbre ---")
    print(f"Resultado del dado: {resultado}")
    print("No podíamos saber este número antes de 'lanzarlo'.")

# Ejecutamos la demostración
demostrar_incertidumbre()
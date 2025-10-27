# Algoritmo 4. Distribución de Probabilidad
# Alan Dorantes Verdin

print("\n--- 4. Distribución de Probabilidad ---")

def es_distribucion_valida(distribucion):
    """
    Verifica si un diccionario representa una distribución de 
    probabilidad discreta válida (si sus probabilidades suman 1).
    """
    # Usamos 'sum()' para sumar todos los valores (probabilidades) del diccionario
    suma_probabilidades = sum(distribucion.values())
    
    # Comparamos con 1. Usamos 'abs' para manejar pequeños errores de punto flotante
    return abs(suma_probabilidades - 1.0) < 0.0001

# Ejemplo 1: Un dado justo (6 caras)
distribucion_dado = {
    1: 1/6,
    2: 1/6,
    3: 1/6,
    4: 1/6,
    5: 1/6,
    6: 1/6
}

# Ejemplo 2: Una moneda cargada
distribucion_moneda = {
    "cara": 0.7,
    "cruz": 0.3
}

# Ejemplo 3: Una distribución inválida
distribucion_invalida = {
    "A": 0.5,
    "B": 0.4
}

print(f"¿Distribución del dado es válida? {es_distribucion_valida(distribucion_dado)}")
print(f"¿Distribución de la moneda es válida? {es_distribucion_valida(distribucion_moneda)}")
print(f"¿Distribución inválida es válida? {es_distribucion_valida(distribucion_invalida)}")
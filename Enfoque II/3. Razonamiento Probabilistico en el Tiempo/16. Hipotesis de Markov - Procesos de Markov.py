# Algoritmo 16. Hipótesis de Markov - Procesos de Markov
# Alan Dorantes Verdin

print("\n--- 16. Hipótesis de Markov - Procesos de Markov ---")

import random

# Usamos la misma matriz de transición del subtema 15
matriz_transicion = {
    'Sol': {'Sol': 0.8, 'Lluvia': 0.2},
    'Lluvia': {'Sol': 0.4, 'Lluvia': 0.6}
}

def simular_cadena_markov(estado_inicial, num_pasos):
    """
    Simula una secuencia de 'num_pasos' de una Cadena de Markov.
    """
    estado_actual = estado_inicial
    secuencia = [estado_actual]
    
    for _ in range(num_pasos):
        # La propiedad de Markov está aquí:
        # Solo necesitamos 'estado_actual', no los estados anteriores.
        
        # Obtenemos las probabilidades de transición desde el estado actual
        probs = matriz_transicion[estado_actual]
        
        # Elegimos el siguiente estado basado en esas probabilidades
        if random.random() < probs['Sol']:
            estado_actual = 'Sol'
        else:
            estado_actual = 'Lluvia'
            
        secuencia.append(estado_actual)
        
    return secuencia

# Generamos una secuencia de 10 días
secuencia_clima = simular_cadena_markov('Sol', 10)
print(f"Secuencia de clima simulada (10 días):")
print(" -> ".join(secuencia_clima))
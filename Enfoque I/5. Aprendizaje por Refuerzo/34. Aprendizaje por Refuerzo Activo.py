# Algoritmo 34. Aprendizaje por Refuerzo Activo
# Alan Dorantes Verdin

import numpy as np # type: ignore
import random

# --- Simulador del Entorno (El Agente NO ve este código) ---
# (El agente solo usa la función 'tomar_paso')

def get_estado_inicial():
    """El agente siempre empieza en el estado 0."""
    return 0

def tomar_paso(estado, accion):
    """
    Esta función es el "mundo".
    El agente dice (estado, accion) y el mundo devuelve (siguiente_estado, recompensa).
    """
    if estado == 2 or estado == 3:
        # Los estados terminales no tienen salida
        return estado, 0 

    # --- Probabilidades (resbaladizo) ---
    prob_exito = 0.8
    prob_fallo = 0.2 # (se queda en el sitio)
    
    # --- Determinar el movimiento ---
    siguiente_estado = -1
    
    # 1. Calcular el estado "objetivo"
    if accion == 'izquierda':
        estado_objetivo = estado - 1
    else: # 'derecha'
        estado_objetivo = estado + 1
    
    # 2. Simular si la acción tuvo éxito o falló
    if random.random() < prob_exito:
        s_intento = estado_objetivo
    else:
        s_intento = estado # Fallo, se queda en el sitio
        
    # 3. Comprobar colisiones con muros (estados -1 y 4)
    if s_intento < 0 or s_intento > 3:
        siguiente_estado = estado # Chocó, se queda en el sitio
    else:
        siguiente_estado = s_intento
        
    # 4. Obtener la recompensa por LLEGAR al siguiente_estado
    recompensa = 0
    if siguiente_estado == 2:
        recompensa = -1 # Pozo
    elif siguiente_estado == 3:
        recompensa = 1  # Tesoro
        
    return siguiente_estado, recompensa

print("\n--- Configuración del Entorno (Simulador) Lista ---")
print("El agente solo puede llamar a 'tomar_paso(s, a)'\n")

# --- 34. Aprendizaje por Refuerzo Activo (Ejemplo con Q-Learning) ---
print("--- 34. Aprendizaje por Refuerzo Activo ---")

# (Funciones de ayuda que se explicarán en los subtemas 35 y 36)
def seleccionar_accion_epsilon_greedy(Q, estado, epsilon):
    if random.random() < epsilon:
        return random.choice(['izquierda', 'derecha']) # Explorar
    else:
        # Explotar
        return 'izquierda' if Q[estado, 0] > Q[estado, 1] else 'derecha'

def q_learning_para_activo(episodios, alfa=0.1, gamma=0.9, epsilon=0.1):
    print("Iniciando RL Activo (Q-Learning)...")
    
    Q = np.zeros((4, 2)) # Q[estado, accion]
    acciones_map = {'izquierda': 0, 'derecha': 1}
    acciones_idx = {0: 'izquierda', 1: 'derecha'}

    for ep in range(episodios):
        estado = get_estado_inicial()
        
        while estado != 2 and estado != 3:
            
            # 1. El agente "Activo" DECIDE qué acción tomar
            accion_str = seleccionar_accion_epsilon_greedy(Q, estado, epsilon)
            accion_idx = acciones_map[accion_str]
            
            # 2. Interactúa con el mundo
            siguiente_estado, recompensa = tomar_paso(estado, accion_str)
            
            # 3. Aprende de la experiencia (Actualización de Q-Learning)
            q_futuro_max = 0 if (siguiente_estado == 2 or siguiente_estado == 3) else np.max(Q[siguiente_estado])
            error_td = (recompensa + gamma * q_futuro_max) - Q[estado, accion_idx]
            Q[estado, accion_idx] = Q[estado, accion_idx] + alfa * error_td
            
            estado = siguiente_estado

    # 4. Al final, el agente "Activo" ha aprendido una política
    politica_optima = {s: acciones_idx[np.argmax(Q[s])] for s in [0, 1]}
    return Q, politica_optima

# --- Ejemplo de uso ---
_, politica_activa = q_learning_para_activo(episodios=1000)
print(f"Política óptima aprendida por el agente ACTIVO: {politica_activa}\n")
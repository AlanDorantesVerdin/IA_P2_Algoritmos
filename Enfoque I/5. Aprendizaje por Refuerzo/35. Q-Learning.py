# Algoritmo 35. Q-Learning
# Alan Dorantes Verdin

import random
import numpy as np # type: ignore

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

# --- 35. Q-Learning ---
print("\n--- 35. Q-Learning ---")

# (Función de ayuda de 36)
def seleccionar_accion_epsilon_greedy(Q, estado, epsilon):
    if random.random() < epsilon:
        return random.choice(['izquierda', 'derecha']) 
    else:
        return 'izquierda' if Q[estado, 0] > Q[estado, 1] else 'derecha'

def q_learning(episodios, alfa=0.1, gamma=0.9, epsilon=0.1):
    print("Iniciando Q-Learning...")
    
    # 1. Inicializar la tabla Q(s, a)
    Q = np.zeros((4, 2)) # 4 estados, 2 acciones
    acciones_map = {'izquierda': 0, 'derecha': 1}
    acciones_idx = {0: 'izquierda', 1: 'derecha'}

    for ep in range(episodios):
        estado = get_estado_inicial()
        
        while estado != 2 and estado != 3:
            
            accion_str = seleccionar_accion_epsilon_greedy(Q, estado, epsilon)
            accion_idx = acciones_map[accion_str]
            
            siguiente_estado, recompensa = tomar_paso(estado, accion_str)
            
            # --- EL NÚCLEO DE Q-LEARNING (Paso 35) ---
            
            # 2. Calcular el 'valor objetivo' (Target)
            # Primero, encontrar el valor de la mejor acción futura: max_a' Q(s', a')
            if siguiente_estado == 2 or siguiente_estado == 3:
                q_futuro_max = 0.0 # Estados terminales no tienen futuro
            else:
                q_futuro_max = np.max(Q[siguiente_estado])
            
            # Valor objetivo = r + gamma * max_a' Q(s', a')
            valor_objetivo = recompensa + gamma * q_futuro_max
            
            # 3. Calcular el Error TD (la 'sorpresa')
            error_td = valor_objetivo - Q[estado, accion_idx]
            
            # 4. Actualizar Q(s, a)
            Q[estado, accion_idx] = Q[estado, accion_idx] + alfa * error_td
            # -------------------------------------------
            
            estado = siguiente_estado

    politica_optima = {s: acciones_idx[np.argmax(Q[s])] for s in [0, 1]}
    return Q, politica_optima

# --- Ejemplo de uso ---
tabla_Q, politica_q = q_learning(episodios=5000)
print("\nTabla Q(s, a) aprendida:")
print("  Acc: Izquierda  Derecha")
print(f"  s=0: {tabla_Q[0, 0]:.3f}     {tabla_Q[0, 1]:.3f}")
print(f"  s=1: {tabla_Q[1, 0]:.3f}     {tabla_Q[1, 1]:.3f}")
print(f"Política óptima: {politica_q}\n")
# Algoritmo 36. Exploración vs Explotación
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


print("\n--- 36. Exploración vs. Explotación ---")

def seleccionar_accion_epsilon_greedy(Q, estado, epsilon):
    """
    Decide si explorar o explotar (Concepto 36).
    """
    # 1. Generar número aleatorio
    if random.random() < epsilon:
        # 2. EXPLORACIÓN (Pasa 'epsilon' % de las veces)
        print(f"  (s={estado}) ¡Explorando! (Acción aleatoria)")
        return random.choice(['izquierda', 'derecha'])
    else:
        # 3. EXPLOTACIÓN (Pasa '1-epsilon' % de las veces)
        print(f"  (s={estado}) ¡Explotando! (Mejor Q)")
        # Devuelve la mejor acción según la tabla Q
        if Q[estado, 0] > Q[estado, 1]:
            return 'izquierda' # (Índice 0)
        else:
            return 'derecha' # (Índice 1)

# --- Algoritmo de Q-Learning (mostrando dónde se usa Epsilon-Greedy) ---

def q_learning_con_exploracion(episodios, alfa=0.1, gamma=0.9, epsilon=0.1):
    print("Iniciando Q-Learning (enfocándonos en Epsilon-Greedy)...")
    
    Q = np.zeros((4, 2)) 
    acciones_map = {'izquierda': 0, 'derecha': 1}
    
    # (Ejecutamos solo 3 episodios para poder ver la traza de exploración)
    for ep in range(3):
        print(f"\n--- Episodio {ep+1} ---")
        estado = get_estado_inicial()
        paso = 0
        while estado != 2 and estado != 3 and paso < 10:
            
            # --- AQUÍ SE USA EL CONCEPTO 36 ---
            accion_str = seleccionar_accion_epsilon_greedy(Q, estado, epsilon)
            accion_idx = acciones_map[accion_str]
            # ---------------------------------
            
            siguiente_estado, recompensa = tomar_paso(estado, accion_str)
            
            # (Actualización Q-Learning ...)
            q_futuro_max = 0 if (siguiente_estado == 2 or siguiente_estado == 3) else np.max(Q[siguiente_estado])
            error_td = (recompensa + gamma * q_futuro_max) - Q[estado, accion_idx]
            Q[estado, accion_idx] = Q[estado, accion_idx] + alfa * error_td
            
            estado = siguiente_estado
            paso += 1
    
    return Q

# --- Ejemplo de uso ---
# (Usamos un epsilon alto (0.5) para forzar la exploración en la demo)
_ = q_learning_con_exploracion(episodios=3, epsilon=0.5)

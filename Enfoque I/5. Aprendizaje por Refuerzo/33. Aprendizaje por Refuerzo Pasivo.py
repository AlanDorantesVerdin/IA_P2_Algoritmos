# Algoritmo 33. Aprendizaje por Refuerzo Pasivo
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

def rl_pasivo_td(politica_fija, episodios, alfa=0.1, gamma=0.9):
    """
    Aprende U(s) para una política fija usando TD Learning.
    """
    print("Iniciando RL Pasivo (TD Learning)...")
    
    # 1. Inicializar Utilidades U(s) a 0
    # (Usamos un array de numpy para 4 estados)
    U = np.zeros(4)
    
    for ep in range(episodios):
        estado = get_estado_inicial()
        
        # Simular un episodio (hasta llegar a un estado terminal)
        while estado != 2 and estado != 3:
            
            # 1. Obtener la acción de la POLÍTICA FIJA
            accion = politica_fija[estado]
            
            # 2. Tomar el paso en el mundo
            siguiente_estado, recompensa = tomar_paso(estado, accion)
            
            # 3. Calcular el "Error TD" (la sorpresa)
            # error = [recompensa_inmediata + utilidad_futura] - utilidad_actual
            error_td = (recompensa + gamma * U[siguiente_estado]) - U[estado]
            
            # 4. Actualizar U(s)
            U[estado] = U[estado] + alfa * error_td
            
            estado = siguiente_estado # Moverse al siguiente estado
            
    print(f"TD Learning completado tras {episodios} episodios.")
    return U

# --- Ejemplo de uso ---
print("--- 33. Aprendizaje por Refuerzo Pasivo (TD Learning) ---")

# Política Fija: 0='derecha', 1='derecha' (2 y 3 son terminales)
politica_fija_td = {0: 'derecha', 1: 'derecha'}

utilidades_aprendidas_td = rl_pasivo_td(politica_fija_td, episodios=1000)
print("Utilidades U(s) aprendidas (política: siempre 'derecha'):")
print(f"  U(0): {utilidades_aprendidas_td[0]:.3f}")
print(f"  U(1): {utilidades_aprendidas_td[1]:.3f}")
print(f"  U(2): {utilidades_aprendidas_td[2]:.3f} (Debería ser -1)")
print(f"  U(3): {utilidades_aprendidas_td[3]:.3f} (Debería ser +1)")
print("\n")
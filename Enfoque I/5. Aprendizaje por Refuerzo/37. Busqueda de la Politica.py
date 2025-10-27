# Algoritmo 37. Búsqueda de la Política
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

print("\n--- 37. Búsqueda de la Política (REINFORCE) ---")

def softmax(x):
    """Calcula probabilidades desde 'preferencias' (logits)."""
    # Restar el máximo previene overflow numérico (e^1000)
    e_x = np.exp(x - np.max(x)) 
    return e_x / e_x.sum(axis=0)

class PolicySearchAgent:
    def __init__(self, n_estados, n_acciones, alfa=0.01, gamma=0.9):
        self.n_estados = n_estados
        self.n_acciones = n_acciones
        self.alfa = alfa # Tasa de aprendizaje
        self.gamma = gamma
        
        # 1. PARAMETRIZACIÓN DE LA POLÍTICA
        # H(s, a) son las "preferencias" o "logits" (nuestros pesos theta)
        # Inicializamos todas las preferencias a 0 (política 50/50)
        self.preferencias_H = np.zeros((n_estados, n_acciones))
        
        # Mapeo de acciones
        self.acciones_map = {'izquierda': 0, 'derecha': 1}
        self.acciones_idx = {0: 'izquierda', 1: 'derecha'}

    def get_politica(self, estado):
        """Calcula P(a|s) para un estado usando softmax."""
        preferencias_estado = self.preferencias_H[estado]
        return softmax(preferencias_estado)

    def seleccionar_accion(self, estado):
        """Muestrea una acción de la política actual."""
        if estado == 2 or estado == 3: # Terminal
            return None, None
            
        probabilidades = self.get_politica(estado)
        
        # Muestrear (ej. si probs=[0.7, 0.3], 70% chance de índice 0)
        accion_idx = np.random.choice([0, 1], p=probabilidades)
        
        return self.acciones_idx[accion_idx], accion_idx

    def actualizar_politica(self, episodio_historia):
        """
        Actualiza los pesos de la política (H) usando REINFORCE
        al final de un episodio.
        """
        
        # episodio_historia = [(estado, accion_idx, recompensa), ...]
        
        # 1. Calcular Retornos Descontados (G_t) para CADA paso
        retornos_G = []
        G_t = 0.0
        # Iteramos hacia atrás desde el final del episodio
        for (s, a_idx, r) in reversed(episodio_historia):
            G_t = r + self.gamma * G_t
            retornos_G.insert(0, G_t) # [G_0, G_1, ..., G_T]
            
        # (Opcional: normalizar retornos para estabilizar)
        retornos_G = np.array(retornos_G)
        if len(retornos_G) > 0 and retornos_G.std() > 0:
            retornos_G = (retornos_G - retornos_G.mean()) / (retornos_G.std() + 1e-8)

        # 2. Actualizar las preferencias (pesos theta)
        for t in range(len(episodio_historia)):
            estado, accion_idx, recompensa = episodio_historia[t]
            G_t = retornos_G[t] # El retorno desde ese paso
            
            # 3. Calcular el Gradiente de la Log-Probabilidad
            probabilidades = self.get_politica(estado)
            
            # grad_log_pi = [d(logP)/dH_0, d(logP)/dH_1]
            grad_log_pi = -probabilidades.copy() # Para las acciones NO tomadas
            grad_log_pi[accion_idx] = 1 - probabilidades[accion_idx] # Para la SÍ tomada
            
            # 4. Actualización del Gradiente (REINFORCE)
            # theta = theta + alfa * G_t * grad_log_pi
            self.preferencias_H[estado] = self.preferencias_H[estado] + self.alfa * G_t * grad_log_pi

# --- Bucle de entrenamiento ---
agente_ps = PolicySearchAgent(n_estados=4, n_acciones=2, alfa=0.01)
episodios = 5000
recompensas_totales = []

for ep in range(episodios):
    estado = get_estado_inicial()
    episodio_historia = []
    recompensa_ep = 0
    max_pasos = 100  # Evitar episodios infinitos
    pasos = 0
    
    while pasos < max_pasos:
        # 1. Usar la política para seleccionar acción
        accion_str, accion_idx = agente_ps.seleccionar_accion(estado)
        
        if accion_str is None: # Llegó a estado terminal
            break
            
        # 2. Tomar paso
        siguiente_estado, recompensa = tomar_paso(estado, accion_str)
        
        # 3. Guardar la transición (s, a, r)
        episodio_historia.append((estado, accion_idx, recompensa))
        recompensa_ep += recompensa
        estado = siguiente_estado
        pasos += 1
        
        # Verificar si llegamos a un estado terminal
        if estado == 2 or estado == 3:
            break
        
    # 4. Actualizar la política al final del episodio
    if len(episodio_historia) > 0:
        agente_ps.actualizar_politica(episodio_historia)
    recompensas_totales.append(recompensa_ep)
    
    if ep % 1000 == 0:
        promedio = np.mean(recompensas_totales[-100:]) if len(recompensas_totales) >= 100 else np.mean(recompensas_totales)
        print(f"Episodio {ep}... Recompensa media: {promedio:.2f}")

print("\nEntrenamiento REINFORCE completado.")
print("\nPolítica final (Probabilidades):")
probs_s0 = agente_ps.get_politica(0)
probs_s1 = agente_ps.get_politica(1)
print(f"  s=0: Izq={probs_s0[0]:.2f}, Der={probs_s0[1]:.2f}")
print(f"  s=1: Izq={probs_s1[0]:.2f}, Der={probs_s1[1]:.2f} (Debería preferir Izquierda)")
print("")
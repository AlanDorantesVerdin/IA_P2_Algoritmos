# Algoritmo 27. Iteración de Valores
# Alan Dorantes Verdin

# --- Definición del MDP (Mundo-Línea) ---

# 1. Estados
estados = [0, 1, 2, 3]
estados_terminales = [2, 3]

# 2. Acciones
acciones = ['izquierda', 'derecha']

# 3. Factor de Descuento
gamma = 0.9

# 4. Recompensas R(s')
recompensas = {
    0: 0,
    1: 0,
    2: -1, # Pozo
    3: 1   # Tesoro
}

# 5. Transiciones T(s, a) -> [(prob, s_siguiente), ...]
transiciones = {
    0: {
        'izquierda': [(0.8, 0), (0.2, 0)], # Choca con muro, 100% queda en 0
        'derecha':   [(0.8, 1), (0.2, 0)]  # 80% éxito, 20% fallo
    },
    1: {
        'izquierda': [(0.8, 0), (0.2, 1)],
        'derecha':   [(0.8, 2), (0.2, 1)]  # 80% va al pozo, 20% queda en 1
    },
    # Estados terminales: no tienen transiciones de salida
    2: {},
    3: {}
}

import copy

def iteracion_de_valores(mdp, epsilon=0.01):
    """
    Resuelve el MDP usando Iteración de Valores.
    """
    print("Iniciando Iteración de Valores...")
    
    # 1. Inicializar Utilidad U(s) = 0 para todos los estados
    U = {s: 0 for s in mdp['estados']}
    
    # Extraer datos del MDP
    gamma = mdp['gamma']
    estados = mdp['estados']
    terminales = mdp['estados_terminales']
    trans = mdp['transiciones']
    recompensas = mdp['recompensas']

    iteracion = 0
    while True:
        iteracion += 1
        delta = 0 # Cambio máximo en esta iteración
        U_nueva = U.copy() # Trabajar sobre una copia

        # 2. Iterar sobre cada estado
        for s in estados:
            if s in terminales:
                # La utilidad de un estado terminal es solo su recompensa
                U_nueva[s] = recompensas[s]
                continue

            # 3. Calcular la utilidad esperada para CADA acción 'a'
            utilidades_acciones = []
            for a in trans[s]:
                q_sa = 0 # Valor Q(s, a)
                
                # 4. Sumar sobre todos los posibles resultados s'
                # Sum_s' [ T(s, a, s') * (R(s') + gamma * U(s')) ]
                for (prob, s_siguiente) in trans[s][a]:
                    # Nota: R(s') es la recompensa por LLEGAR a s'
                    q_sa += prob * (recompensas[s_siguiente] + gamma * U[s_siguiente])
                
                utilidades_acciones.append(q_sa)
            
            # 5. La nueva utilidad de 's' es el MÁXIMO de las acciones
            U_nueva[s] = max(utilidades_acciones)
            
            # 6. Registrar el cambio máximo
            delta = max(delta, abs(U_nueva[s] - U[s]))

        # 7. Actualizar U
        U = U_nueva
        
        # 8. Criterio de convergencia
        if delta < epsilon * (1 - gamma) / gamma:
            print(f"Convergencia alcanzada en {iteracion} iteraciones.")
            return U

# --- Ejemplo de uso (con el MDP definido al inicio) ---
print("\n--- 27. Iteración de Valores ---")

# Creamos el objeto MDP
mdp_linea = {
    'estados': estados,
    'acciones': acciones,
    'transiciones': transiciones,
    'recompensas': recompensas,
    'gamma': gamma,
    'estados_terminales': estados_terminales
}

utilidades_optimas = iteracion_de_valores(mdp_linea)
print("Utilidades óptimas U(s) encontradas:")
for s, u in utilidades_optimas.items():
    print(f"  U({s}): {u:.3f}")
print("")
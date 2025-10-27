# Algoritmo 28. Iteración de Políticas
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

def iteracion_de_politicas(mdp):
    """
    Resuelve el MDP usando Iteración de Políticas.
    """
    print("Iniciando Iteración de Políticas...")
    
    # Extraer datos del MDP
    estados = mdp['estados']
    terminales = mdp['estados_terminales']
    trans = mdp['transiciones']
    recompensas = mdp['recompensas']
    gamma = mdp['gamma']

    # 1. Inicializar Utilidad U(s) = 0
    U = {s: 0 for s in estados}
    
    # 2. Inicializar Política pi(s) aleatoriamente
    pi = {s: 'derecha' for s in estados if s not in terminales}
    
    iteracion = 0
    while True:
        iteracion += 1
        print(f"\nIteración {iteracion} de Política:")
        print(f"  Política actual: {pi}")

        # --- Paso 1: Evaluación de Política ---
        # (Versión simplificada: iterar K veces la ec. de Bellman)
        # (Una versión completa resolvería un sistema de ecuaciones)
        k_evaluacion = 20
        for _ in range(k_evaluacion):
            U_eval = U.copy()
            for s in estados:
                if s in terminales:
                    U_eval[s] = recompensas[s]
                    continue
                
                # Obtener la acción de la política FIJA
                a = pi[s]
                
                # Calcular la utilidad SIGUIENDO esa acción
                q_sa = 0
                for (prob, s_siguiente) in trans[s][a]:
                    q_sa += prob * (recompensas[s_siguiente] + gamma * U[s_siguiente])
                
                U_eval[s] = q_sa
            U = U_eval
        
        print(f"  Utilidades evaluadas: { {s: round(u, 2) for s, u in U.items()} }")

        # --- Paso 2: Mejora de Política ---
        politica_estable = True
        
        for s in estados:
            if s in terminales:
                continue

            # Acción antigua
            a_antigua = pi[s]
            
            # Encontrar la MEJOR acción 'a' según U
            mejor_a = None
            mejor_q = -float('inf')
            
            for a in trans[s]:
                q_sa = 0
                for (prob, s_siguiente) in trans[s][a]:
                    q_sa += prob * (recompensas[s_siguiente] + gamma * U[s_siguiente])
                
                if q_sa > mejor_q:
                    mejor_q = q_sa
                    mejor_a = a
            
            # Actualizar la política
            pi[s] = mejor_a
            
            # 3. Comprobar si la política cambió
            if a_antigua != mejor_a:
                politica_estable = False

        # 4. Criterio de convergencia
        if politica_estable:
            print(f"\nPolítica estable encontrada en {iteracion} iteraciones.")
            return pi, U

# --- Ejemplo de uso ---
print("\n--- 28. Iteración de Políticas ---")

# Creamos el objeto MDP
mdp_linea = {
    'estados': estados,
    'acciones': acciones,
    'transiciones': transiciones,
    'recompensas': recompensas,
    'gamma': gamma,
    'estados_terminales': estados_terminales
}

(politica_optima, utilidades) = iteracion_de_politicas(mdp_linea)
print("\nPolítica óptima pi(s) encontrada:")
print(f"  {politica_optima}")
print("Utilidades óptimas U(s) encontradas:")
for s, u in utilidades.items():
    print(f"  U({s}): {u:.3f}")
print("")
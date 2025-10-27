# Algoritmo 26. Valor de la Información
# Alan Dorantes Verdin

print("\n--- 26. Valor de la Información (VPI) ---")

# Cálculo de la Utilidad Esperada (EU)
prob_sol = 0.5
prob_lluvia = 0.5

# Utilidades asociadas a cada resultado
U_sol_si = 80
U_lluvia_si = 70
U_sol_no = 100
U_lluvia_no = 0

# Cálculo de la Utilidad Esperada para cada decisión
eu_si_paraguas = (prob_sol * U_sol_si) + (prob_lluvia * U_lluvia_si)
eu_no_paraguas = (prob_sol * U_sol_no) + (prob_lluvia * U_lluvia_no)

# 1. Utilidad máxima sin información (del paso 25)
eu_max_sin_info = eu_si_paraguas # 75

# 2. Utilidad esperada CON información perfecta
# Si sé que hará sol, elijo la mejor acción para sol (No llevar = 100)
U_optima_sol = max(U_sol_si, U_sol_no)
# Si sé que lloverá, elijo la mejor acción para lluvia (Sí llevar = 70)
U_optima_lluvia = max(U_lluvia_si, U_lluvia_no)

eu_con_info = (prob_sol * U_optima_sol) + (prob_lluvia * U_optima_lluvia)
print(f"Utilidad Esperada CON Información Perfecta: {eu_con_info}")

# 3. VPI
vpi = eu_con_info - eu_max_sin_info
print(f"Valor de la Información Perfecta (VPI): {vpi}\n")
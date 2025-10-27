# Algoritmo 25. Redes de Decisión
# Alan Dorantes Verdin

# Una Red Bayesiana con nodos de Decisión y Utilidad
print("\n--- 25. Redes de Decisión ---")

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

print(f"Utilidad Esperada (Llevar Paraguas): {eu_si_paraguas}")
print(f"Utilidad Esperada (No Llevar Paraguas): {eu_no_paraguas}")
print(f"Decisión óptima: Llevar Paraguas.\n")
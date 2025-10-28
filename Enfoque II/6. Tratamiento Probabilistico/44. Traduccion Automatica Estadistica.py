# Algoritmo 44. Traducción Automática Estadística
# Alan Dorantes Verdin

from collections import defaultdict

def entrenar_ibm_model1(corpus_paralelo, iteraciones_em=10):
    """
    Aprende las probabilidades t(e|f) usando EM.
    """
    
    # 1. Inicialización (Probabilidades t(e|f) uniformes)
    # t[ingles][frances]
    prob_t = defaultdict(lambda: defaultdict(float))
    vocab_frances = set()
    
    # Recolectar vocabulario y inicializar
    for (f_frase, e_frase) in corpus_paralelo:
        for f in f_frase:
            vocab_frances.add(f)
            
    # Inicialización uniforme
    for (f_frase, e_frase) in corpus_paralelo:
        for e in e_frase:
            for f in f_frase:
                prob_t[e][f] = 1.0 / len(vocab_frances)

    # --- 2. Bucle EM ---
    for _ in range(iteraciones_em):
        
        # conteo[e][f] (Conteo esperado)
        conteo_ef = defaultdict(lambda: defaultdict(float))
        # total_f[f] (Total esperado)
        total_f = defaultdict(float)
        
        # --- PASO E (Expectation) ---
        for (f_frase, e_frase) in corpus_paralelo:
            for e in e_frase:
                # Calcular denominador (suma de t(e|f) para esta e)
                suma_denominador = sum(prob_t[e][f_k] for f_k in f_frase)
                
                if suma_denominador == 0: continue
                
                for f in f_frase:
                    # Calcular responsabilidad (conteo "suave")
                    responsabilidad = prob_t[e][f] / suma_denominador
                    
                    # Acumular conteos esperados
                    conteo_ef[e][f] += responsabilidad
                    total_f[f] += responsabilidad
                    
        # --- PASO M (Maximization) ---
        # Recalcular probabilidades t(e|f)
        for e, f_dict in conteo_ef.items():
            for f, conteo in f_dict.items():
                if total_f[f] > 0:
                    prob_t[e][f] = conteo / total_f[f]
                    
    return prob_t

# --- Ejecución ---
# Corpus paralelo (Francés -> Inglés)
corpus = [
    (["la", "maison"], ["the", "house"]),
    (["la", "maison", "bleue"], ["the", "blue", "house"]),
    (["le", "chien"], ["the", "dog"])
]

# Entrenar
probabilidades_t = entrenar_ibm_model1(corpus, iteraciones_em=10)

print(f"\n--- 44. Traducción Estadística (IBM Model 1) ---")
print("Probabilidades t(ingles | frances) aprendidas:")

print(f"\nProbabilidades para t( ... | 'la'):")
print(f"  t(the | la) = {probabilidades_t['the']['la']:.4f}")
print(f"  t(house | la) = {probabilidades_t['house']['la']:.4f}")

print(f"\nProbabilidades para t( ... | 'maison'):")
print(f"  t(the | maison) = {probabilidades_t['the']['maison']:.4f}")
print(f"  t(house | maison) = {probabilidades_t['house']['maison']:.4f}")
print(f"  t(blue | maison) = {probabilidades_t['blue']['maison']:.4f}")
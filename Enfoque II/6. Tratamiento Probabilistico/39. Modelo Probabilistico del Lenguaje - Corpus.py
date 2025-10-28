# Algoritmo 39. Modelo Probabilístico del Lenguaje - Corpus
# Alan Dorantes Verdin

from collections import defaultdict

def entrenar_modelo_bigrama(corpus_texto):
    """
    Entrena un modelo de bigramas simple (conteo de frecuencias).
    Devuelve un diccionario: {palabra_anterior: {palabra_siguiente: conteo}}
    """
    # Tokenizar el corpus (separar por palabras)
    # Agregamos tokens de INICIO y FIN para cada oración
    oraciones = corpus_texto.lower().split('.')
    
    # modelo[palabra_anterior][palabra_siguiente] = conteo
    modelo = defaultdict(lambda: defaultdict(int))
    
    for oracion in oraciones:
        palabras = ["<INICIO>"] + oracion.split() + ["<FIN>"]
        if len(palabras) < 2:
            continue
            
        # Crear los bigramas
        for i in range(len(palabras) - 1):
            palabra_anterior = palabras[i]
            palabra_siguiente = palabras[i+1]
            
            # Contar la ocurrencia
            modelo[palabra_anterior][palabra_siguiente] += 1
            
    return modelo

def predecir_siguiente_palabra(modelo, palabra_anterior):
    """
    Predice la palabra más probable siguiente usando el modelo de bigrama.
    """
    palabra_anterior = palabra_anterior.lower()
    
    if palabra_anterior not in modelo:
        return "[Palabra desconocida]"
        
    # Obtener todas las posibles palabras siguientes
    posibles_siguientes = modelo[palabra_anterior]
    
    # Encontrar la palabra con el conteo más alto (más probable)
    palabra_mas_probable = max(posibles_siguientes, key=posibles_siguientes.get)
    
    return palabra_mas_probable

# --- Ejecución ---
corpus = (
    "El auto es rojo. El auto es rápido."
    "Mi auto rojo es nuevo. El perro es rápido."
)

modelo_bigrama = entrenar_modelo_bigrama(corpus)

print("\n--- 39. Modelo de Lenguaje (Bigrama) ---")
print(f"Modelo aprendido (parcial): P( ... | 'auto' )")
print(f"-> {modelo_bigrama['auto']}")

# Probar el modelo
palabra_anterior = "El"
prediccion = predecir_siguiente_palabra(modelo_bigrama, palabra_anterior)
print(f"\nDespués de '{palabra_anterior}', la palabra más probable es: '{prediccion}'")

palabra_anterior = "auto"
prediccion = predecir_siguiente_palabra(modelo_bigrama, palabra_anterior)
print(f"Después de '{palabra_anterior}', la palabra más probable es: '{prediccion}'")
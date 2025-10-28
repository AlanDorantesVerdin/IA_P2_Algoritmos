# Algoritmo 42. Recuperación de Datos
# Alan Dorantes Verdin

import numpy as np
from collections import Counter
import math

# --- 1. Definir Funciones ---

def calcular_tf(termino, documento_tokenizado):
    """Calcula la Frecuencia de Término (TF) logarítmica."""
    conteo = documento_tokenizado.count(termino)
    return 1 + math.log10(conteo) if conteo > 0 else 0

def calcular_idf(termino, corpus_tokenizado):
    """Calcula la Frecuencia Inversa de Documento (IDF)."""
    N = len(corpus_tokenizado)
    num_docs_con_termino = sum(1 for doc in corpus_tokenizado if termino in doc)
    if num_docs_con_termino == 0:
        return 0
    return math.log10(N / num_docs_con_termino)

def similitud_coseno(vec1, vec2):
    """Calcula la similitud coseno entre dos vectores numpy."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)

# --- 2. Algoritmo de Búsqueda ---

def buscar_tf_idf(query, corpus):
    """
    Busca en el corpus usando el modelo TF-IDF.
    """
    # Tokenizar corpus y consulta
    corpus_tokenizado = [doc.lower().split() for doc in corpus]
    query_tokenizada = query.lower().split()
    
    # Crear vocabulario (todos los términos únicos)
    vocabulario = set(t for doc in corpus_tokenizado for t in doc)
    vocab_lista = sorted(list(vocabulario))
    
    # --- Vectorizar Corpus (TF-IDF) ---
    vectores_corpus = []
    for doc_tok in corpus_tokenizado:
        vec = np.zeros(len(vocab_lista))
        for i, termino_vocab in enumerate(vocab_lista):
            tf = calcular_tf(termino_vocab, doc_tok)
            idf = calcular_idf(termino_vocab, corpus_tokenizado)
            vec[i] = tf * idf
        vectores_corpus.append(vec)
        
    # --- Vectorizar Consulta (TF-IDF) ---
    vec_query = np.zeros(len(vocab_lista))
    for i, termino_vocab in enumerate(vocab_lista):
        tf = calcular_tf(termino_vocab, query_tokenizada)
        idf = calcular_idf(termino_vocab, corpus_tokenizado)
        vec_query[i] = tf * idf

    # --- 3. Calcular Similitud ---
    resultados = []
    for i in range(len(corpus)):
        sim = similitud_coseno(vec_query, vectores_corpus[i])
        resultados.append((sim, corpus[i]))
        
    # Ordenar por similitud (de mayor a menor)
    resultados.sort(key=lambda x: x[0], reverse=True)
    return resultados

# --- Ejecución ---
corpus_docs = [
    "El perro persigue al gato",
    "El gato persigue al ratón",
    "El perro come croquetas",
    "El ratón come queso"
]
query = "perro y gato"

resultados_busqueda = buscar_tf_idf(query, corpus_docs)

print(f"\n--- 42. Recuperación de Datos (TF-IDF) ---")
print(f"Consulta: '{query}'")
print("Resultados (ordenados por relevancia):")
for sim, doc in resultados_busqueda:
    print(f"  Similitud: {sim:.4f} | Documento: '{doc}'")
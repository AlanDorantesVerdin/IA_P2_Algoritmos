# Algoritmo 43. Extracción de Información
# Alan Dorantes Verdin

import re

def extraer_info_regex(texto):
    """
    Extrae correos electrónicos y números de teléfono usando RegEx.
    """
    
    # 1. Definir los patrones (RegEx)
    # Patrón simple para correo electrónico
    patron_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Patrón simple para teléfono (ej. 555-1234 o (555) 123-4567)
    patron_telefono = r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
    
    # 2. Encontrar todas las coincidencias
    correos = re.findall(patron_email, texto)
    telefonos = re.findall(patron_telefono, texto)
    
    # 3. Devolver la información estructurada
    return {"correos": correos, "telefonos": telefonos}

# --- Ejecución ---
texto_no_estructurado = """
El contacto principal es Juan Pérez en juan.perez@ejemplo.com.
Puede llamar al (800) 555-1234 para soporte.
El contacto secundario es ana.g@mi-sitio.org
o en el móvil 333-456-7890.
"""

info_extraida = extraer_info_regex(texto_no_estructurado)

print(f"\n--- 43. Extracción de Información (RegEx) ---")
print(f"Texto de entrada:\n{texto_no_estructurado}")
print("Información Estructurada Extraída:")
print(f"  Correos: {info_extraida['correos']}")
print(f"  Teléfonos: {info_extraida['telefonos']}")
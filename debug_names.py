"""
Arregla los 6 casos restantes donde el nombre exacto tiene caracteres
acentuados o especiales que el regex no encontró.
"""
import os

HTML_PATH = os.path.join("50_visionarios", "index.html")

# Lista de reemplazos directos: (texto_img_unsplash_ACTUAL, nuevo_src)
# Tenemos que identificar qué imagen de Unsplash está en la card fallida
# por posición en el archivo. Usamos el nombre APROXIMADO que sí existe.

# Las 6 cards fallidas:
# 1. Miguel Roldán       -> slide_07.jpg
# 2. Antonio Muñoz Ariza -> slide_20.jpg
# 3. Paco Rosales        -> slide_22.jpg
# 4. Javier Campos       -> slide_23.jpg
# 5. Almudena Villegas   -> slide_26.jpg
# 6. Javier Alcalá de la Moneda -> slide_27.jpg

# Estrategia: abrir el HTML en binario, encontrar el texto en raw bytes
with open(HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Imprimir los bloques de texto alrededor de cada persona buscada
search_terms = [
    "Rold",         # Miguel Roldán
    "Mu",           # Muñoz
    "Rosales",      # Paco Rosales
    "Javier C",     # Javier Campos
    "Almudena",     # Almudena Villegas
    "Alcal",        # Javier Alcalá
    "Aguilar",      # Marian Aguilar
]

for term in search_terms:
    pos = content.find(term)
    if pos == -1:
        print(f"NOT FOUND: '{term}'")
    else:
        snippet = content[max(0,pos-100):pos+200]
        print(f"\n=== '{term}' at pos {pos} ===")
        print(repr(snippet[:300]))

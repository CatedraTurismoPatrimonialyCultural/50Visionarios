"""
Reemplaza las 6 imagenes faltantes buscando los bloques exactos del HTML
y la URL de Unsplash JUSTO ANTES de cada nombre en el mismo article.
"""
import re
import os

HTML_PATH = os.path.join("50_visionarios", "index.html")

# Cada entrada: (fragmento_unico_del_nombre_en_h3, imagen_a_poner)
# El fragmento debe ser único en el HTML para identificar la card
FIXES = [
    # (texto que aparece en h3, nueva imagen)
    ("Miguel Roldán</h3>", "images/slide_07.jpg"),
    ("Paco Rosales</h3>", "images/slide_22.jpg"),
    ("Javier Campos</h3>", "images/slide_23.jpg"),
    ("Almudena Villegas</h3>", "images/slide_26.jpg"),
    ("Antonio Muñoz Ariza</h3>", "images/slide_20.jpg"),
    ("Javier Alcalá de la Moneda</h3>", "images/slide_27.jpg"),
]

with open(HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

for h3_text, img_path in FIXES:
    # Encontrar posición del nombre en h3
    pos_name = content.find(h3_text)
    if pos_name == -1:
        print(f"NO ENCONTRADO: {h3_text}")
        continue
    
    # Buscar hacia ATRÁS desde pos_name hasta el último <img src="https://images.unsplash
    # dentro de los últimos 2000 chars (el article completo es ~500 chars)
    search_area = content[max(0, pos_name-2000):pos_name]
    
    # Encontrar el último src="https://images.unsplash.com/..." en esa área
    matches = list(re.finditer(r'src="(https://images\.unsplash\.com/[^"]+)"', search_area))
    if not matches:
        print(f"NO HAY UNSPLASH antes de: {h3_text}")
        continue
    
    last_match = matches[-1]
    old_url = last_match.group(1)
    
    # Reemplazar la PRIMERA ocurrencia de esa URL exacta en el HTML
    # (solo la que corresponde a esta card)
    abs_pos = max(0, pos_name-2000) + last_match.start()
    
    # Reemplazar en el contenido
    # Construir el nuevo src
    old_src = f'src="{old_url}"'
    new_src = f'src="{img_path}"'
    
    # Reemplazar SOLO en el área cercana (para no afectar otras cards con misma URL)
    area_start = max(0, pos_name-2000)
    area_end = pos_name + len(h3_text)
    
    area = content[area_start:area_end]
    
    # Reemplazar última ocurrencia de old_src en el área
    last_occ = area.rfind(old_src)
    if last_occ == -1:
        print(f"No se encontró src exacto en area: {h3_text}")
        continue
    
    new_area = area[:last_occ] + new_src + area[last_occ+len(old_src):]
    content = content[:area_start] + new_area + content[area_end:]
    
    print(f"OK: {h3_text.replace('</h3>','')} -> {img_path}")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! HTML actualizado con las 6 imagenes restantes.")

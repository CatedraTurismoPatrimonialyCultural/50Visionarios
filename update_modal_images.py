"""
Actualiza las imagenes dentro de los MODALES del HTML.
En cada modal, la imagen esta en:
  <div class="w-full md:w-2/5 ...">
    <img src="UNSPLASH" ...>
  </div>
  <div class="w-full md:w-3/5 ...">
    <h2>NOMBRE</h2>

Buscamos por h2 y reemplazamos la img que esta JUSTO ANTES.
"""
import re
import os

HTML_PATH = os.path.join("50_visionarios", "index.html")

# Mapeo: texto en h2 del modal -> imagen local
# (los h2 tienen el nombre de la INSTITUCION o PERSONA)
MODAL_MAP = {
    # h2 text -> imagen
    "Fundación Palacio de Viana": "images/slide_01.jpg",
    "Mezquita-Catedral de Córdoba": "images/slide_02.jpg",
    "Museo Arqueológico de Córdoba": "images/slide_03.jpg",
    "Antonio Vallejo Triano": "images/slide_06.jpg",
    "Consejería de Turismo, Cultura y Deporte": "images/slide_04.jpg",
    "Casa Sefarad": "images/slide_05.jpg",
    "Foto por incorporar": None,  # slide 7 - Patios (con nombre generico)
    "Manuel Murillo Estévez": "images/slide_08.jpg",
    "Antonio Monterroso Checa": "images/slide_09.jpg",
    "Isabel Albás Vives": "images/slide_10.jpg",
    "Eduardo Lucena": "images/slide_12.jpg",
    "Anselmo Córdoba": "images/slide_13.jpg",
    "Área de Turismo de la Subbética Cordobesa": "images/slide_14.jpg",
    "Antonio Caño": "images/slide_15.jpg",
    "Asociación de Empresarios de Alojamientos de Córdoba": "images/slide_16.jpg",
    "Confederación de Empresarios de Córdoba (CEC)": "images/slide_17.jpg",
    "Restaurante Noor (★★★ Michelin)": "images/slide_18.jpg",
    "Investigación en Gastronomía Patrimonial": "images/slide_19.jpg",
    "Antonio Muñoz Ariza": "images/slide_20.jpg",
    "Restaurante El Churrasco": "images/slide_21.jpg",
    "Paco Rosales": "images/slide_22.jpg",
    "Javier Campos": "images/slide_23.jpg",
    "Finca El Capricho": "images/slide_24.jpg",
    "Cofradía Gastronómica del Rabo de Toro Cordobés": "images/slide_25.jpg",
    "Almudena Villegas": "images/slide_26.jpg",
    "Javier Alcalá de la Moneda": "images/slide_27.jpg",
    "ACORA  Asociación Oleícola de Córdoba": "images/slide_29.jpg",
    "Teresa Jiménez  Guitarrista": "images/slide_30.jpg",
    "David Pino  Músico": "images/slide_31.jpg",
    "Lola Pérez  Flamenco y Cultura": "images/slide_32.jpg",
    "Antonio Manuel Rodriguez Ramos": "images/slide_33.jpg",
    "Desiderio Vaquerizo  Universidad de Córdoba": "images/slide_34.jpg",
    "Mª Ángeles Jordano Barbudo": "images/slide_35.jpg",
    "Mª Ángeles Recio Ramírez,": "images/slide_11.jpg",
    "Carmen Balbuena  Turismo y Patrimonio": "images/slide_37.jpg",
    "Manuel Rivera  Universidad de Córdoba": "images/slide_38.jpg",
    "Nuria Ceular  \x0bVillamandos": "images/slide_39.jpg",
    "José Antonio Fernández Gallardo  Universidad de Córdoba": "images/slide_40.jpg",
    "Teresa Ávalos Ureña": "images/slide_41.jpg",
    "Paloma López-Sidro": "images/slide_42.jpg",
    "Walada de la Mata": "images/slide_43.jpg",
    "Dr. Tomás López-Guzmán": "images/slide_36.jpg",
    "Juan Salado – Palacio de Congresos": "images/slide_44.jpg",
    "Rocío Aceña - Directora del Castillo de Almodovar": "images/slide_45.jpg",
    "Fernando Lara de Vicente": "images/slide_46.jpg",
    "Ricardo Hernández Rojas": "images/slide_47.jpg",
    "Esther bueno Gallardo": "images/slide_48.jpg",
    "Narcisa Ruiz Rodriguez": "images/slide_49.jpg",
    # Modal 7 tiene "Foto por incorporar" en h2 -> Miguel Roldán
}

# También el modal para "Foto por incorporar" de Patios
# buscaremos por contexto

with open(HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

total_fixed = 0

for h2_text, img_path in MODAL_MAP.items():
    if img_path is None:
        continue
    
    # Buscar <h2 ...>h2_text</h2> en el HTML
    h2_pattern = f'<h2 class="font-serif text-3xl md:text-4xl text-white mb-2">{re.escape(h2_text)}</h2>'
    pos_h2 = content.find(f'>{h2_text}</h2>')
    
    if pos_h2 == -1:
        # Try with escaped text
        pos_h2 = content.find(h2_text)
        if pos_h2 == -1:
            print(f"MODAL NO ENCONTRADO: {h2_text}")
            continue
    
    # Buscar hacia atras la imagen de Unsplash (dentro del modal, ~500 chars antes)
    search_area = content[max(0, pos_h2-800):pos_h2]
    
    matches = list(re.finditer(r'src="(https://images\.unsplash\.com/[^"]+)"', search_area))
    if not matches:
        print(f"Sin Unsplash antes del modal h2: {h2_text}")
        continue
    
    last_match = matches[-1]
    old_url = last_match.group(1)
    old_src = f'src="{old_url}"'
    new_src = f'src="{img_path}"'
    
    area_start = max(0, pos_h2-800)
    area_end = pos_h2 + len(h2_text)
    area = content[area_start:area_end]
    
    last_occ = area.rfind(old_src)
    if last_occ == -1:
        print(f"  src no encontrado exacto: {h2_text}")
        continue
    
    new_area = area[:last_occ] + new_src + area[last_occ+len(old_src):]
    content = content[:area_start] + new_area + content[area_end:]
    total_fixed += 1
    print(f"  MODAL OK: {h2_text[:50]} -> {img_path}")

# Fix especial para "Foto por incorporar" que es Miguel Roldan (modal-7)
# En ese modal h2 = "Foto por incorporar", p = "Asociación de los Patios"
patios_pos = content.find("Asociación de los Patios de Córdoba</h2>")
if patios_pos == -1:
    # buscar por el subtitulo que es único
    # "Foto por incorporar" h2 con Patios en p
    pass

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal modales actualizados: {total_fixed}")

# Verificar cuántas URLs de Unsplash quedan
import re as re2
remaining = re2.findall(r'src="(https://images\.unsplash[^"]+)"', content)
print(f"URLs Unsplash restantes: {len(remaining)}")

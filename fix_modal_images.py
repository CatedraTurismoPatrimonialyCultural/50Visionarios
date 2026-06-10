"""
Actualiza las imagenes en los bloques <div id="modal-X"> del HTML.
En cada modal la estructura es:
  <div id="modal-N" ...>
    ...
    <img src="UNSPLASH" ...>  <- imagen del modal (izquierda)
    ...
    <h2>NOMBRE</h2>
"""
import re
import os

HTML_PATH = os.path.join("50_visionarios", "index.html")

# Mapeo: fragmento del h2 -> imagen local
# Usamos el inicio del h2 text para identificar el modal
MODAL_MAP = [
    ("Fundación Palacio de Viana", "images/slide_01.jpg"),
    ("Mezquita-Catedral de Córdoba", "images/slide_02.jpg"),
    ("Museo Arqueológico de Córdoba", "images/slide_03.jpg"),
    ("Antonio Vallejo Triano", "images/slide_06.jpg"),
    ("Consejería de Turismo, Cultura y Deporte", "images/slide_04.jpg"),
    ("Casa Sefarad", "images/slide_05.jpg"),
    ("Manuel Murillo Estévez", "images/slide_08.jpg"),
    ("Antonio Monterroso Checa", "images/slide_09.jpg"),
    ("Isabel Albás Vives", "images/slide_10.jpg"),
    ("Eduardo Lucena", "images/slide_12.jpg"),
    ("Anselmo Córdoba", "images/slide_13.jpg"),
    ("Área de Turismo de la Subbética Cordobesa", "images/slide_14.jpg"),
    ("Antonio Caño", "images/slide_15.jpg"),
    ("Asociación de Empresarios de Alojamientos de Córdoba", "images/slide_16.jpg"),
    ("Confederación de Empresarios de Córdoba (CEC)", "images/slide_17.jpg"),
    ("Restaurante Noor", "images/slide_18.jpg"),
    ("Investigación en Gastronomía Patrimonial", "images/slide_19.jpg"),
    ("Antonio Muñoz Ariza", "images/slide_20.jpg"),
    ("Restaurante El Churrasco", "images/slide_21.jpg"),
    ("Paco Rosales", "images/slide_22.jpg"),
    ("Javier Campos", "images/slide_23.jpg"),
    ("Finca El Capricho", "images/slide_24.jpg"),
    ("Cofradía Gastronómica del Rabo de Toro", "images/slide_25.jpg"),
    ("Almudena Villegas", "images/slide_26.jpg"),
    ("Javier Alcalá de la Moneda", "images/slide_27.jpg"),
    ("ACORA", "images/slide_29.jpg"),
    ("Teresa Jiménez", "images/slide_30.jpg"),
    ("David Pino", "images/slide_31.jpg"),
    ("Lola Pérez", "images/slide_32.jpg"),
    ("Antonio Manuel Rodriguez Ramos", "images/slide_33.jpg"),
    ("Desiderio Vaquerizo", "images/slide_34.jpg"),
    ("Mª Ángeles Jordano Barbudo", "images/slide_35.jpg"),
    ("Mª Ángeles Recio Ramírez", "images/slide_11.jpg"),
    ("Carmen Balbuena", "images/slide_37.jpg"),
    ("Manuel Rivera", "images/slide_38.jpg"),
    ("Nuria Ceular", "images/slide_39.jpg"),
    ("José Antonio Fernández Gallardo", "images/slide_40.jpg"),
    ("Teresa Ávalos Ureña", "images/slide_41.jpg"),
    ("Paloma López-Sidro", "images/slide_42.jpg"),
    ("Walada de la Mata", "images/slide_43.jpg"),
    ("Dr. Tomás López-Guzmán", "images/slide_36.jpg"),
    ("Juan Salado", "images/slide_44.jpg"),
    ("Rocío Aceña", "images/slide_45.jpg"),
    ("Fernando Lara de Vicente", "images/slide_46.jpg"),
    ("Ricardo Hernández Rojas", "images/slide_47.jpg"),
    ("Esther bueno Gallardo", "images/slide_48.jpg"),
    ("Narcisa Ruiz Rodriguez", "images/slide_49.jpg"),
]

with open(HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Dividir el HTML en bloques de modales
# Cada modal empieza con <div id="modal-
modal_blocks = re.split(r'(?=<div id="modal-\d+)', content)

new_blocks = []
total_fixed = 0

for block in modal_blocks:
    fixed_block = block
    
    for h2_fragment, img_path in MODAL_MAP:
        if h2_fragment not in block:
            continue
        
        # Este bloque contiene este modal
        # Reemplazar la imagen de Unsplash en este bloque
        def replace_unsplash(m):
            return f'src="{img_path}"'
        
        new_block, n = re.subn(
            r'src="https://images\.unsplash\.com/[^"]+"',
            replace_unsplash,
            fixed_block,
            count=1  # Solo la primera (la imagen del modal)
        )
        
        if n > 0:
            fixed_block = new_block
            total_fixed += 1
            print(f"  MODAL OK: {h2_fragment[:40]} -> {img_path}")
        break  # Solo un mapeo por bloque
    
    new_blocks.append(fixed_block)

content = ''.join(new_blocks)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal modales actualizados: {total_fixed}")
remaining = re.findall(r'src="(https://images\.unsplash[^"]+)"', content)
print(f"URLs Unsplash restantes: {len(remaining)}")
if remaining:
    for r in remaining[:5]:
        print(f"  {r[:80]}")

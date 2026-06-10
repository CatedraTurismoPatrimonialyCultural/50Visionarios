"""
SOLUCIÓN DEFINITIVA: Reconstruye el HTML de 50_visionarios/index.html
reemplazando TODAS las URLs de Unsplash por imágenes locales.

Estrategia: dividir por article y por modal, en cada bloque
reemplazar la PRIMERA img src de Unsplash por la imagen local correspondiente
basándonos en el NÚMERO de orden del bloque (card 1 = slide_01, etc.)
"""
import re
import os

HTML_PATH = os.path.join("50_visionarios", "index.html")

# MAPEO DEFINITIVO: número de tarjeta (1-based, orden en el HTML) -> archivo imagen
# Basado en el análisis visual de las slides del PPTX
CARD_TO_IMAGE = {
    1: "images/slide_01.jpg",   # Fundación Palacio de Viana / Leopoldo Izquierdo
    2: "images/slide_02.jpg",   # Mezquita-Catedral / Jose Joaquin
    3: "images/slide_03.jpg",   # Museo Arqueológico / Irene Maclino
    4: "images/slide_06.jpg",   # Antonio Vallejo Triano / Medina Azahara
    5: "images/slide_04.jpg",   # Consejería / Gonzalo Herreros
    6: "images/slide_05.jpg",   # Casa Sefarad / Sebastian de la Obra
    7: "images/slide_07.jpg",   # Miguel Roldán / Patios
    8: "images/slide_08.jpg",   # Manuel Murillo / Cofradías
    9: "images/slide_09.jpg",   # Antonio Monterroso / Arqueólogo
    10: "images/slide_10.jpg",  # Isabel Albás / Alcalde Cultura
    11: "images/slide_12.jpg",  # Eduardo Lucena / Delegado Territorial
    12: "images/slide_13.jpg",  # Anselmo Córdoba / Destilerías (logo)
    13: "images/slide_14.jpg",  # Catalina Molina / Subbética
    14: "images/slide_15.jpg",  # Antonio Caño / OPC (logo)
    15: "images/slide_16.jpg",  # Elena Rizos / AHECOR
    16: "images/slide_17.jpg",  # Antonia Alcántara / CEC
    17: "images/slide_18.jpg",  # Paco Morales / Noor
    18: "images/slide_19.jpg",  # Leonardo Gallardo / Gastronomía
    19: "images/slide_20.jpg",  # Antonio Muñoz Ariza / Bodegas Campos
    20: "images/slide_21.jpg",  # Rafael Carrillo / El Churrasco
    21: "images/slide_22.jpg",  # Paco Rosales / Grupo Rosales
    22: "images/slide_23.jpg",  # Javier Campos / Ermita la Candelaria
    23: "images/slide_24.jpg",  # Rafael San Miguel / Finca El Capricho
    24: "images/slide_25.jpg",  # Ricardo Rojas / Cofradía Gastronómica
    25: "images/slide_26.jpg",  # Almudena Villegas / Historiadora
    26: "images/slide_27.jpg",  # Javier Alcalá / DOP Baena
    27: "images/slide_29.jpg",  # Macarena Sánchez / ACORA
    28: "images/slide_30.jpg",  # Teresa Jiménez / Guitarrista
    29: "images/slide_31.jpg",  # David Pino / Músico
    30: "images/slide_32.jpg",  # Lola Pérez / Flamenco
    31: "images/slide_33.jpg",  # Antonio Manuel / Flamenco
    32: "images/slide_34.jpg",  # Desiderio Vaquerizo / UCO
    33: "images/slide_35.jpg",  # Mª Ángeles Jordano / Arte
    34: "images/slide_11.jpg",  # Mª Ángeles Recio / Profesora (logo)
    35: "images/slide_37.jpg",  # Carmen Balbuena / Turismo
    36: "images/slide_38.jpg",  # Manuel Rivera / UCO
    37: "images/slide_39.jpg",  # Nuria Ceular / Decana
    38: "images/slide_40.jpg",  # José Antonio Fernández / UCO
    39: "images/slide_41.jpg",  # Teresa Ávalos / KOL Flamenco
    40: "images/slide_42.jpg",  # Paloma / Guía Turística
    41: "images/slide_43.jpg",  # Walada de la Mata / Guías
    42: "images/slide_36.jpg",  # Dr. Tomás López-Guzmán / Cátedra
    43: "images/slide_44.jpg",  # Juan Salado / Palacio Congresos
    44: "images/slide_45.jpg",  # Rocío Aceña / Castillo Almodóvar
    45: "images/slide_46.jpg",  # Fernando Lara / Gestión cultural
    46: "images/slide_47.jpg",  # Ricardo Hernández Rojas / Cátedra
    47: "images/slide_48.jpg",  # Esther Bueno Gallardo / UCO
    48: "images/slide_49.jpg",  # Narcisa Ruiz Rodriguez / Diputada Turismo
}

with open(HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Dividir el HTML por article (tarjetas)
# Cada article es una tarjeta
parts = re.split(r'(?=<article\s)', content)

print(f"Total partes divididas por article: {len(parts)}")

new_parts = []
card_counter = 0

for part in parts:
    if part.strip().startswith('<article'):
        card_counter += 1
        if card_counter in CARD_TO_IMAGE:
            img_path = CARD_TO_IMAGE[card_counter]
            # Reemplazar TODAS las URLs de unsplash en esta tarjeta
            n_replacements = len(re.findall(r'src="https://images\.unsplash[^"]*"', part))
            part = re.sub(
                r'src="https://images\.unsplash[^"]*"',
                f'src="{img_path}"',
                part
            )
            if n_replacements > 0:
                print(f"  Card {card_counter:02d}: {n_replacements} img reemplazada(s) -> {img_path}")
        else:
            print(f"  Card {card_counter:02d}: SIN MAPEO (fuera de rango)")
    new_parts.append(part)

content = ''.join(new_parts)

# Ahora actualizar los MODALES (div id="modal-N")
modal_parts = re.split(r'(?=<div id="modal-\d+)', content)
print(f"\nTotal partes de modal: {len(modal_parts)}")

new_modal_parts = []
for part in modal_parts:
    m = re.search(r'id="modal-(\d+)"', part)
    if m:
        modal_n = int(m.group(1))
        if modal_n in CARD_TO_IMAGE:
            img_path = CARD_TO_IMAGE[modal_n]
            n = len(re.findall(r'src="https://images\.unsplash[^"]*"', part))
            part = re.sub(
                r'src="https://images\.unsplash[^"]*"',
                f'src="{img_path}"',
                part,
                count=1  # solo la primera imagen del modal (el retrato)
            )
            if n > 0:
                print(f"  Modal {modal_n:02d}: img reemplazada -> {img_path}")
    new_modal_parts.append(part)

content = ''.join(new_modal_parts)

# Verificar resultado
remaining = re.findall(r'src="(https://images\.unsplash[^"]+)"', content)
print(f"\nURLs Unsplash restantes en HTML: {len(remaining)}")

# Guardar
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"HTML guardado: {HTML_PATH}")
print("DONE!")

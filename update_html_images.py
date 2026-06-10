"""
Actualiza el HTML de 50_visionarios/index.html
reemplazando las URLs de Unsplash por las imágenes locales extraídas del PPTX.

Mapeo basado en el orden de las cards en el HTML:
Card 1  (modal-1)  -> Leopoldo Izquierdo         -> slide_01.jpg
Card 2  (modal-2)  -> Jose Joaquin               -> slide_02.jpg
Card 3  (modal-3)  -> Irene Maclino Navarro       -> slide_03.jpg
Card 4  (modal-4)  -> Antonio Vallejo Triano      -> slide_06.jpg  (slide_04 es Gonzalo)
... etc.

NOTA: Las cards HTML NO siguen el mismo orden que el JSON original.
Vamos a hacer el mapeo por NOMBRE (card title) -> imagen correspondiente.
"""
import re
import os

# Mapeo nombre (en el HTML) -> archivo de imagen local
# Basado en el análisis del HTML y los slides del PPTX
NAME_TO_IMAGE = {
    # Gestión Patrimonial (cards HTML)
    "Fundación Palacio de Viana": "images/slide_01.jpg",           # Leopoldo Izquierdo
    "Mezquita-Catedral de Córdoba": "images/slide_02.jpg",         # Jose Joaquin
    "Museo Arqueológico de Córdoba": "images/slide_03.jpg",        # Irene Maclino
    "Antonio Vallejo Triano": "images/slide_06.jpg",               # Medina Azahara
    "Consejería de Turismo, Cultura y Deporte": "images/slide_04.jpg",  # Gonzalo Herreros
    "Casa Sefarad": "images/slide_05.jpg",                         # Sebastian de la Obra
    "Miguel Roldán": "images/slide_07.jpg",                        # Patios de Córdoba
    "Manuel Murillo Estévez": "images/slide_08.jpg",               # Cofradías
    "Antonio Monterroso Checa": "images/slide_09.jpg",             # Arqueólogo
    "Isabel Albás Vives": "images/slide_10.jpg",                   # Teniente Alcalde Cultura
    "Eduardo Lucena": "images/slide_12.jpg",                       # Delegado Territorial
    "Anselmo Córdoba": "images/slide_13.jpg",                      # Destilerías (sin foto -> logo)
    "Área de Turismo de la Subbética Cordobesa": "images/slide_14.jpg",  # Catalina Molina
    "Antonio Caño": "images/slide_15.jpg",                         # OPC (sin foto -> logo)
    "Asociación de Empresarios de Alojamientos de Córdoba": "images/slide_16.jpg",  # Elena Rizos
    "Confederación de Empresarios de Córdoba (CEC)": "images/slide_17.jpg",  # Antonia Alcantara
    # Gastronomía
    "Restaurante Noor (★★★ Michelin)": "images/slide_18.jpg",       # Paco Morales
    "Investigación en Gastronomía Patrimonial": "images/slide_19.jpg",  # Leonardo Gallardo
    "Antonio Muñoz Ariza": "images/slide_20.jpg",                  # Bodegas Campos
    "Restaurante El Churrasco": "images/slide_21.jpg",             # Rafael Carrillo
    "Paco Rosales": "images/slide_22.jpg",                         # Grupo Rosales
    "Javier Campos": "images/slide_23.jpg",                        # Ermita la Candelaria
    "Finca El Capricho": "images/slide_24.jpg",                    # Rafael San Miguel
    "Cofradía Gastronómica del Rabo de Toro Cordobés": "images/slide_25.jpg",  # Ricardo Rojas
    "Almudena Villegas": "images/slide_26.jpg",                    # Historiadora
    "Javier Alcalá de la Moneda": "images/slide_27.jpg",           # DOP Baena
    "ACORA  Asociación Oleícola de Córdoba": "images/slide_29.jpg", # Macarena Sánchez
    "Teresa Jiménez  Guitarrista": "images/slide_30.jpg",          # Teresa Guitar
    "David Pino  Músico": "images/slide_31.jpg",                   # David Pino
    "Lola Pérez  Flamenco y Cultura": "images/slide_32.jpg",       # Lola Perez
    "Antonio Manuel Rodriguez Ramos": "images/slide_33.jpg",       # Antonio Manuel
    # Academia/Innovación
    "Desiderio Vaquerizo  Universidad de Córdoba": "images/slide_34.jpg",  # Desiderio
    "Mª Ángeles Jordano Barbudo": "images/slide_35.jpg",           # Ma Angeles Jordano
    "Mª Ángeles Recio Ramírez,": "images/slide_11.jpg",            # slide 11 (logo - sin foto)
    "Carmen Balbuena  Turismo y Patrimonio": "images/slide_37.jpg",  # Carmen Balbuena
    "Manuel Rivera  Universidad de Córdoba": "images/slide_38.jpg",  # Manuel Rivera
    "Nuria Ceular  \x0bVillamandos": "images/slide_39.jpg",         # Nuria Ceular
    "José Antonio Fernández Gallardo  Universidad de Córdoba": "images/slide_40.jpg",
    # KOL
    "Teresa Ávalos Ureña": "images/slide_41.jpg",                  # Teresa Avalos
    "Paloma López-Sidro": "images/slide_42.jpg",                   # Paloma
    "Walada de la Mata": "images/slide_43.jpg",                    # Walada
    # Extras (slides 44-50 que son personas adicionales)
    "Dr. Tomás López-Guzmán": "images/slide_36.jpg",               # Ricardo Hernandez (slide 36)
    "Juan Salado – Palacio de Congresos": "images/slide_44.jpg",
    "Rocío Aceña - Directora del Castillo de Almodovar": "images/slide_45.jpg",
    "Fernando Lara de Vicente": "images/slide_46.jpg",
    "Ricardo Hernández Rojas": "images/slide_47.jpg",
    "Esther bueno Gallardo": "images/slide_48.jpg",
    "Narcisa Ruiz Rodriguez": "images/slide_49.jpg",
}

# Slides sin foto (solo logo) -> mantener unsplash pero especial
NO_PHOTO_SLIDES = {13, 15}  # Anselmo Córdoba, Antonio Caño (solo logo en ppt)

HTML_PATH = os.path.join("50_visionarios", "index.html")

def main():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    replacements_done = 0
    
    for name, img_path in NAME_TO_IMAGE.items():
        # Comprobar que la imagen existe
        full_img_path = os.path.join("50_visionarios", img_path)
        if not os.path.exists(full_img_path):
            print(f"  ⚠️  Imagen no encontrada: {full_img_path} (para: {name})")
            continue
        
        # Buscar el bloque de article que contiene este nombre en h3 o p
        # Estrategia: buscar src="https://images.unsplash..." dentro del contexto del nombre
        # Para cada card, el nombre aparece en <h3>...</h3> cerca de una <img src="unsplash">
        
        # Construimos un patrón que encuentre la imagen de Unsplash JUSTO ANTES del nombre
        # dentro del mismo article
        
        # Patrón simplificado: buscar pares (src de unsplash, nombre) en el mismo bloque de 200 chars
        escaped_name = re.escape(name)
        
        # Buscar <img ...unsplash...> seguido por cualquier cosa y luego el nombre, 
        # dentro del mismo article (~400 chars aprox)
        pattern = r'(<img src=")(https://images\.unsplash\.com/[^"]+)("(?:[^>]*)>(?:(?!</article>).){0,500}?' + escaped_name + r')'
        
        def replace_img(m):
            return m.group(1) + img_path + m.group(3)
        
        new_content, count = re.subn(pattern, replace_img, content, flags=re.DOTALL)
        
        if count > 0:
            content = new_content
            replacements_done += count
            print(f"  ✅ [{count}x] {name} -> {img_path}")
        else:
            print(f"  ❌ NO encontrado en HTML: '{name}'")
    
    if replacements_done > 0:
        with open(HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ HTML actualizado: {replacements_done} imágenes reemplazadas")
        print(f"   Archivo: {HTML_PATH}")
    else:
        print("\n⚠️  No se realizaron cambios")

if __name__ == "__main__":
    main()

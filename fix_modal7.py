import re, os

HTML_PATH = os.path.join("50_visionarios", "index.html")

with open(HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Dividir en bloques de modal
modal_blocks = re.split(r'(?=<div id="modal-\d+)', content)

new_blocks = []
for block in modal_blocks:
    if 'id="modal-7"' in block and 'unsplash' in block.lower():
        # Reemplazar la imagen de Unsplash por slide_07.jpg (Miguel Roldan)
        new_block = re.sub(
            r'src="https://images\.unsplash\.com/[^"]+"',
            'src="images/slide_07.jpg"',
            block,
            count=1
        )
        # También actualizar el h2 que dice "Foto por incorporar"
        new_block = new_block.replace(
            '>Foto por incorporar</h2>',
            '>Miguel Roldán</h2>'
        )
        # Actualizar el subtitulo p
        new_block = new_block.replace(
            'Asociación de los Patios de Córdoba</p>',
            'Presidente — Asociación de los Patios de Córdoba</p>'
        )
        new_blocks.append(new_block)
        print("Modal-7 (Miguel Roldan) actualizado con slide_07.jpg")
    else:
        new_blocks.append(block)

content = ''.join(new_blocks)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

# Verificar
remaining = re.findall(r'src="(https://images\.unsplash[^"]+)"', content)
print(f"URLs Unsplash restantes: {len(remaining)}")

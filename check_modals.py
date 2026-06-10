import re, os

HTML_PATH = os.path.join("50_visionarios", "index.html")

with open(HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Dividir en modales
modal_blocks = re.split(r'(?=<div id="modal-\d+)', content)
print(f"Total bloques (incluyendo inicio): {len(modal_blocks)}")

# Contar cuales modales aun tienen unsplash
modal_with_unsplash = []
for block in modal_blocks:
    if 'id="modal-' in block and 'unsplash' in block.lower():
        # Extraer modal ID
        m = re.search(r'id="(modal-\d+)"', block)
        modal_id = m.group(1) if m else "?"
        # Extraer h2
        h2 = re.search(r'<h2[^>]*>([^<]+)</h2>', block)
        h2_text = h2.group(1) if h2 else "?"
        modal_with_unsplash.append((modal_id, h2_text))

print(f"\nModales con Unsplash aun: {len(modal_with_unsplash)}")
for mid, h2 in modal_with_unsplash:
    print(f"  {mid}: {h2[:60]}")

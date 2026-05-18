import sys

# Set output to UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('slides_content.txt', 'r', encoding='utf-16le') as f:
    content = f.read()
    print(content[:5000])

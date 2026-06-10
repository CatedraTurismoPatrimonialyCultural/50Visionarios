import re
with open('50_visionarios/index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
matches = re.findall(r'src="(https://images\.unsplash[^"]+)"', content)
print(f'Remaining Unsplash URLs: {len(matches)}')
for m in matches[:20]:
    print(' ', m[:100])

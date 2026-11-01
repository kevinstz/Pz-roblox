import re
from collections import Counter

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

classes = re.findall(r'<Item class="([^"]+)"', text)
counts = Counter(classes)
for cls, count in counts.most_common():
    print(f"{cls:25s}: {count}")

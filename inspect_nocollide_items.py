import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's see: what parts have "Puerta" in their name?
matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)

puertas = []
exterior_walls_nocollide = []

for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', block)
    if m_name and m_cc:
        name = m_name.group(1)
        cc = m_cc.group(1)
        if name.startswith('Puerta_') and cc == 'false':
            puertas.append((ref, name, cls))
        elif 'exterior' in name.lower() and 'wall' in name.lower() and cc == 'false':
            exterior_walls_nocollide.append((ref, name, cls))

print(f"Total Puerta_ parts with CanCollide=false: {len(puertas)}")
print(f"Total exterior wall parts with CanCollide=false: {len(exterior_walls_nocollide)}")
from collections import Counter
print("Exterior walls with CanCollide=false:", Counter([w[1] for w in exterior_walls_nocollide]))

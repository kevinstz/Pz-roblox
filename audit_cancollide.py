import re
from collections import Counter

types = Counter()
full_names = Counter()
RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    for line in fin:
        if not buffering:
            if '<Item class="Part"' in line or '<Item class="WedgePart"' in line:
                buffering = True
                depth = 1
                buffer = [line]
        else:
            buffer.append(line)
            if '<Item ' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    buffering = False
                    block = "".join(buffer)
                    if '<bool name="CanCollide">false</bool>' in block:
                        m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                        if m_name:
                            name = m_name.group(1)
                            prefix = name.split('_')[0] if '_' in name else name
                            types[prefix] += 1
                            if any(w in name.lower() for w in ['wall', 'muro', 'door', 'puerta', 'roof', 'techo', 'window', 'ventana']):
                                full_names[name.split('|')[0] if '|' in name else name] += 1
                    buffer = []

print("Top prefixes with CanCollide=false:")
for k, v in types.most_common(20):
    print(f"  {k}: {v}")

print("\nStructural elements with CanCollide=false:")
for k, v in full_names.most_common(30):
    print(f"  {k}: {v}")

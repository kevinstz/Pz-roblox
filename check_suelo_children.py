import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_suelo_folder = False
    depth = 0
    children = []
    
    for line in f:
        if '<string name="Name">Suelo</string>' in line:
            in_suelo_folder = True
            depth = 1
            continue
        if in_suelo_folder:
            if '<Item' in line:
                depth += 1
                if depth == 2:
                    m_cls = re.search(r'<Item class="([^"]+)"', line)
                    cls = m_cls.group(1) if m_cls else "Unknown"
                    children.append((cls, line.strip()))
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    break

print(f"Children of Suelo folder: {len(children)}")
for c in children[:20]:
    print(c)

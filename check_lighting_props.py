import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

m = re.search(r'<Item class="Lighting" referent="[^"]+">.*?</Item>', content, re.DOTALL)
if m:
    print("Lighting:")
    print(m.group(0)[:1500])

import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

m = re.search(r'<Item class="LocalScript" referent="R153412">.*?</Item>', content, re.DOTALL)
if m:
    print(m.group(0))

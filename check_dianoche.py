import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

m = re.search(r'<Item class="Script" referent="R153409">.*?<ProtectedString name="Source">(.*?)</ProtectedString>', content, re.DOTALL)
if m:
    print("PZ_DiaNoche source:")
    print(m.group(1))

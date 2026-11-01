import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

match = re.search(r'<Item class="LocalScript" referent="RBXIsoCursorCtrl">.*?<ProtectedString name="Source">(.*?)</ProtectedString>', content, re.DOTALL)
if match:
    src = match.group(1)
    print("IsometricCursorController length:", len(src))
    print(src)

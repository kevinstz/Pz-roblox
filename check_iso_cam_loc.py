import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

# Let's inspect where IsometricCamera is in PZ_Rosewood.rbxlx
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

m = re.search(r'<Item class="LocalScript" referent="R153412">.*?<ProtectedString name="Source">(.*?)</ProtectedString>', content, re.DOTALL)
if m:
    print("Found IsometricCamera source:")
    print(m.group(1)[:500])

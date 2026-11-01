import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pattern = re.compile(r'<Item class="(?:Script|LocalScript)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>.*?<ProtectedString name="Source">(.*?)</ProtectedString>', re.DOTALL)
for m in pattern.finditer(content):
    ref, name, src = m.groups()
    print(f"Name: {name:30s} | Ref: {ref:15s} | Length: {len(src)}")

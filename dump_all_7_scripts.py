import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pattern = re.compile(r'<Item class="(?:Script|LocalScript|ModuleScript)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>.*?<ProtectedString name="Source">(.*?)</ProtectedString>', re.DOTALL)
for match in pattern.finditer(content):
    ref, name, src = match.groups()
    print(f"=== SCRIPT: {name} ({ref}) ===")
    print(src[:1200])
    print("\n" + "="*50 + "\n")

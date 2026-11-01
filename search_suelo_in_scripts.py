import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find all scripts
pattern = re.compile(r'<Item class="(?:Script|LocalScript)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>.*?<ProtectedString name="Source">(.*?)</ProtectedString>', re.DOTALL)
for match in pattern.finditer(content):
    ref, name, src = match.groups()
    if 'suelo' in src.lower():
        print(f"Script '{name}' mentions 'suelo':")
        for line in src.splitlines():
            if 'suelo' in line.lower():
                print(f"  {line.strip()}")
    else:
        print(f"Script '{name}' does NOT mention 'suelo'.")

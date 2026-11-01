import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's find all Scripts / LocalScripts
scripts = re.findall(r'<Item class="(?:LocalScript|Script)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>.*?<ProtectedString name="Source">(.*?)</ProtectedString>', content, re.DOTALL)
print(f'Found {len(scripts)} Scripts')
for ref, name, src in scripts:
    print('Script Name:', name)
    if 'camera' in name.lower() or 'iso' in name.lower() or 'cutaway' in name.lower():
        print(f'=== {name} ===')
        print(src)
        print('='*40)

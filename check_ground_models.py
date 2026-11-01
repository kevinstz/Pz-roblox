import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# TerrenoCircundante
m_terr = re.search(r'<Item class="Part" referent="[^"]+">\s*<Properties>.*?<string name="Name">TerrenoCircundante</string>.*?</Properties>', content, re.DOTALL)
if m_terr:
    print("TerrenoCircundante:")
    print(m_terr.group(0))

# Suelo_Piso_0
m_suelo = re.search(r'<Item class="Model" referent="([^"]+)">\s*<Properties>.*?<string name="Name">Suelo_Piso_0</string>.*?</Properties>', content, re.DOTALL)
if m_suelo:
    print("\nSuelo_Piso_0 Model:")
    print(m_suelo.group(0))

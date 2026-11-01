import re
import math

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

# Let's find all building models in Edificios and calculate their bounding box
# Exactly like BuildingCutawayController does!
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

edif_start = content.find('<string name="Name">Edificios</string>')
edif_end = content.find('</Item>', edif_start + 1000) # find closing of Edificios folder
# In fact let's parse all Models inside Edificios
# Edificios is a Folder
pattern = re.compile(r'<Item class="Model" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>', re.DOTALL)

# Let's find each building's parts and bounding box
# In PZ_Rosewood.rbxlx, buildings have models with Piso_0, Piso_1...
bld_matches = re.finditer(r'<Item class="Model" referent="([^"]+)">\s*<Properties>.*?<string name="Name">(Edificio_[^<]+|Banco_[^<]+|Casa_[^<]+|Clinica_[^<]+|EstacionPolicia_[^<]+|Comisaria_[^<]+|Hotel_[^<]+|Restaurante_[^<]+|Supermercado_[^<]+|Gasolinera_[^<]+|Taller_[^<]+|Bomberos_[^<]+|Juzgado_[^<]+)</string>', content)

buildings = []
for m in bld_matches:
    ref = m.group(1)
    name = m.group(2)
    buildings.append((ref, name, m.start()))

print(f"Found {len(buildings)} buildings:")
for b in buildings:
    print(f"  {b[1]} (ref={b[0]})")

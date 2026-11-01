target_place = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(target_place, 'rb') as f:
    data = f.read()

idx_veh = data.find(b'<string name="Name">Vehiculos</string>')
sub = data[idx_veh:idx_veh+40000]

# find all items in first car
import re
items = re.findall(rb'<Item class="([^"]*)" referent="([^"]*)">\s*<Properties>.*?<string name="Name">([^<]+)</string>', sub, re.DOTALL)
print("Items in vehicle:")
for c, r, n in items[:25]:
    print(f"  {c.decode():15s} {n.decode()}")

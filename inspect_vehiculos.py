target_place = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(target_place, 'rb') as f:
    data = f.read()

idx_veh = data.find(b'<string name="Name">Vehiculos</string>')
if idx_veh != -1:
    print("Found Vehiculos folder at:", idx_veh)
    item_start = data.rfind(b'<Item class="Folder"', 0, idx_veh)
    # print next 10000 bytes
    print(data[idx_veh:idx_veh+10000].decode('utf-8', errors='ignore'))
else:
    print("Vehiculos folder not found!")

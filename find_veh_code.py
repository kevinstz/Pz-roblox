with open(r'C:\Users\julia\Downloads\pz_roblox_b42\build_map.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Vehiculos')
if idx == -1:
    idx = text.find('create_vehicle_model')
print(text[idx-200:idx+800])

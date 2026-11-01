with open(r'C:\Users\julia\Downloads\pz_roblox_b42\pzlib\client_scripts.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('local TILE_STUDS')
print(text[idx:idx+1200])

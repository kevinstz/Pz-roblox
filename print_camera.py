with open(r'C:\Users\julia\Downloads\pz_roblox_b42\pzlib\client_scripts.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('CAMERA')
if idx == -1:
    idx = text.find('Camera')
print(text[idx:idx+800])

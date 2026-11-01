with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\pzlib\iso.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('def floor_image')
print(text[idx:idx+1200])

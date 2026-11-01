target_place = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(target_place, 'rb') as f:
    data = f.read()

idx = data.find(b'<string name="Name">Patrulla_Policial</string>')
sub = data[idx:idx+20000]

import re
matches = re.findall(rb'<string name="Name">(Chasis|Rueda_\d)</string>.*?<CoordinateFrame name="CFrame">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', sub, re.DOTALL)
for m in matches[:10]:
    print(f"{m[0].decode():10s}: X={float(m[1]):.2f}, Y={float(m[2]):.2f}, Z={float(m[3]):.2f}")

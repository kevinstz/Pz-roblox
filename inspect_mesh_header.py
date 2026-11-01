with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\meshes\police_car.mesh', 'rb') as f:
    header = f.read(500)

print(header.decode('utf-8', errors='ignore'))

with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\meshes\police_car.mesh', 'rb') as f:
    data = f.read(64)

print(data[:30])
print(' '.join(f'{b:02x}' for b in data[:30]))

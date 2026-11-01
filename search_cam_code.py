p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("Contains CAMERA_DISTANCE:", "CAMERA_DISTANCE" in content)
print("Contains ISO_PITCH_DEG:", "ISO_PITCH_DEG" in content)
print("Contains BuildingCutawayController:", "BuildingCutawayController" in content)
print("Contains IsometricCursorController:", "IsometricCursorController" in content)

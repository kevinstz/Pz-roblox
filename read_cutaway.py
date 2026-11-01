import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

capturing = False
lines = []

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<string name="Name">BuildingCutawayController</string>' in line:
            capturing = True
            continue
        if capturing:
            if '<ProtectedString name="Source">' in line:
                lines.append(line)
            elif '</ProtectedString>' in line:
                lines.append(line)
                break
            elif lines:
                lines.append(line)

print("".join(lines[:120]))

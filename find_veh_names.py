rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'Police' in line or 'Vehiculo' in line or 'Base.PickUp' in line or 'Car' in line:
            print(f"L{i}: {line.strip()[:100]}")
            if i > 200000:
                break

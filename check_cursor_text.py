rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'Isometric' in line or 'puntero' in line or 'Cursor' in line or 'reticle' in line.lower():
            print(f"Line {i+1}: {line.strip()[:100]}")
            if i > 9670000:
                break

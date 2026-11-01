rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'CursorRing' in line or 'CursorDot' in line or 'CursorLine' in line:
            print(f"Cursor element found at line {i+1}: {line.strip()[:100]}")
            break

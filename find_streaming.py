rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if 'Streaming' in line or 'Stream' in line:
            print(f"Line {idx+1}: {line.strip()}")
            if idx > 200:
                break

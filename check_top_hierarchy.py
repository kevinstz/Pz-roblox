rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if idx < 200:
            if '<Item' in line or '<string name="Name">' in line:
                print(f"{idx+1}: {line.strip()}")

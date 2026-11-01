src = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(src, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if '<Y>-4.0</Y>' in line:
            print(f"Line {i}: {line.strip()}")
        if '<Y>-3.2</Y>' in line:
            print(f"STILL PRESENT: Line {i}: {line.strip()}")

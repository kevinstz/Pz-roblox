rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    count = 0
    for i, line in enumerate(f):
        if '<Y>-3.2</Y>' in line:
            count += 1
            print(f"Match {count} at line {i}: {line.strip()}")
    print("Total matches for <Y>-3.2</Y>:", count)

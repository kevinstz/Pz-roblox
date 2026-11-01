rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'name="Name">Spawn_Rosewood<' in line:
            # print 40 lines before
            target_idx = i
            break

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if target_idx - 35 <= i <= target_idx + 5:
            print(f"{i}: {line}", end="")

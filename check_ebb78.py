rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_ground"

count_ebb7 = 0
count_ebb8 = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "ebb7" in line:
            count_ebb7 += 1
        if "ebb8" in line:
            count_ebb8 += 1

print("ebb7 in backup:", count_ebb7, "ebb8 in backup:", count_ebb8)

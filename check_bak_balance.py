import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_houses"

open_items = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<Item ' in line:
            open_items += 1
        if '</Item>' in line:
            open_items -= 1

print(f"Backup file open items balance: {open_items}")

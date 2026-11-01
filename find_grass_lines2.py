rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
lines_found = []
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if 'blends_grassoverlays_01_' in line:
            lines_found.append(idx + 1)

print(f"Total lines with blends_grassoverlays_01_: {len(lines_found)}")
print(f"Min line: {min(lines_found)}, Max line: {max(lines_found)}")

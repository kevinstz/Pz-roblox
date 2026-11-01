rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx in range(1, 2357377):
        f.readline()
    
    # Now test the loop on next 1000 lines
    buf = []
    in_part = False
    part_depth = 0
    parts_seen = 0
    for idx in range(2357377, 2360000):
        line = f.readline()
        if '<Item class="Part"' in line:
            in_part = True
            part_depth = 1
            buf = [line]
            continue
        if in_part:
            buf.append(line)
            if '<Item' in line:
                part_depth += 1
            if '</Item>' in line:
                part_depth -= 1
                if part_depth == 0:
                    in_part = False
                    parts_seen += 1
                    buf = []

print(f"Test loop processed cleanly! in_part={in_part}, part_depth={part_depth}, parts_seen={parts_seen}")

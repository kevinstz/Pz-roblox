rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    item_lines = []
    in_item = False
    found = False
    for line in f:
        if '<Item class="LocalScript"' in line:
            in_item = True
            item_lines = [line]
            found = False
            continue
        if in_item:
            item_lines.append(line)
            if 'BuildingCutawayController' in line:
                found = True
            if '</Item>' in line:
                if found:
                    print("".join(item_lines[:80]))
                    break
                in_item = False
                item_lines = []

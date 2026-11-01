rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    window = []
    found = False
    for line in f:
        window.append(line)
        if len(window) > 1000:
            window.pop(0)
        if '<string name="Name">BuildingCutawayController</string>' in line:
            # Look backwards in window for <Item
            item_start = 0
            for i in range(len(window)-1, -1, -1):
                if '<Item class="LocalScript"' in window[i]:
                    item_start = i
                    break
            # Now continue reading until </Item>
            lines = window[item_start:]
            for l2 in f:
                lines.append(l2)
                if '</Item>' in l2:
                    break
            print("".join(lines))
            break

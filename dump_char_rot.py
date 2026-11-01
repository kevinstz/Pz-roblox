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
            if 'SurvivorCharacterController' in line:
                found = True
            if '</Item>' in line:
                if found:
                    for i, l in enumerate(item_lines):
                        if 'RenderStepped' in l or 'CFrame' in l or 'lookAt' in l or 'targetLookDir' in l:
                            start = max(0, i - 10)
                            end = min(len(item_lines), i + 35)
                            print(f"Lines around match {i}:")
                            print("".join(item_lines[start:end]))
                            break
                    break
                in_item = False
                item_lines = []

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
                    print("FOUND SurvivorCharacterController! Total lines:", len(item_lines))
                    print("".join(item_lines[:60]))
                    print("\n--- SNIP ---\n")
                    print("".join(item_lines[-50:]))
                    break
                in_item = False
                item_lines = []

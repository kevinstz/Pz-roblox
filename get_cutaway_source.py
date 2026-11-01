rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    collecting = False
    name = None
    source = []
    for line in f:
        if '<Item class="LocalScript"' in line or '<Item class="Script"' in line:
            name = None
            source = []
        if '<string name="Name">' in line and name is None:
            name = line.split('<string name="Name">')[1].split('</string>')[0]
        if '<ProtectedString name="Source">' in line:
            collecting = True
            source = [line]
            continue
        if collecting:
            source.append(line)
            if '</ProtectedString>' in line:
                collecting = False
                if name and "Cutaway" in name:
                    print(f"=== SCRIPT: {name} ===")
                    print("".join(source[:50]))

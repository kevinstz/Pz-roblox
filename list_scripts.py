rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<Item class="LocalScript"' in line or '<Item class="Script"' in line:
            pass
        if '<string name="Name">' in line:
            name = line.split('<string name="Name">')[1].split('</string>')[0]
            if any(k in name for k in ['Camera', 'Cutaway', 'Isometric', 'Survivor', 'PZ_']):
                print(name)

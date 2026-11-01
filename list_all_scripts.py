rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_script = False
    script_class = ""
    script_name = ""
    for line in f:
        if '<Item class="Script"' in line or '<Item class="LocalScript"' in line or '<Item class="ModuleScript"' in line:
            in_script = True
            script_class = line.split('"')[1]
            continue
        if in_script:
            if '<string name="Name">' in line:
                script_name = line.split('>')[1].split('<')[0]
                print(f"Class: {script_class}, Name: {script_name}")
                in_script = False

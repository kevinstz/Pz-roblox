with open(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\apply_house_upgrades.py", "r", encoding="utf-8") as f:
    for line in f:
        if 'UniqueId' in line:
            print(line.strip())

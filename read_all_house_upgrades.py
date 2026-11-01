with open(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\apply_house_upgrades.py", "r", encoding="utf-8") as f:
    text = f.read()
    print("Length of apply_house_upgrades.py:", len(text))
    # print functions defined
    for line in text.splitlines():
        if line.startswith("def ") or line.startswith("BUILDINGS") or "build_house" in line or "apply_" in line:
            print(line)

src = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

in_suelo0 = False
modes = {}

with open(src, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if 'name="Name">Suelo_Piso_0<' in line:
            in_suelo0 = True
            continue
        elif in_suelo0 and ('referent="R33263"' in line or 'name="Name">Suelo_Piso_1<' in line):
            in_suelo0 = False
            break
        if in_suelo0 and '<token name="ModelStreamingMode">' in line:
            mode = line.strip()
            modes[mode] = modes.get(mode, 0) + 1

print("Suelo_Piso_0 chunk streaming modes:", modes)
assert modes.get('<token name="ModelStreamingMode">2</token>', 0) == 88, f"Expected 88 chunks with mode 2, got {modes}"
print("All 88 chunks verified as Persistent (ModelStreamingMode = 2): OK!")

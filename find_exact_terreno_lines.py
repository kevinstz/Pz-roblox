p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    buf = []
    found = False
    for idx, line in enumerate(f, 1):
        if 'name="Name">TerrenoCircundante' in line:
            print(f"TerrenoCircundante at line {idx}")
            for b in buf[-30:]:
                print(b.rstrip())
            break
        buf.append(f"{idx}: {line}")

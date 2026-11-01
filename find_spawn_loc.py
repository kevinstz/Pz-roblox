rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_spawn = False
    lines = []
    for line in f:
        if 'name="Name">Spawn_Rosewood<' in line or in_spawn:
            in_spawn = True
            lines.append(line)
            if len(lines) > 50:
                print("".join(lines))
                break
        elif '<Item class="SpawnLocation"' in line:
            lines = [line]

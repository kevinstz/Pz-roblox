rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_ws = False
    ws_lines = []
    for line in f:
        if '<Item class="Workspace"' in line:
            in_ws = True
            ws_lines = [line]
            continue
        if in_ws:
            ws_lines.append(line)
            if '</Properties>' in line:
                for l in ws_lines:
                    if 'Stream' in l or 'stream' in l or 'Streaming' in l:
                        print(l.strip())
                break

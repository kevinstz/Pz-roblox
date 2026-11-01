rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    buf = []
    cap = False
    for line in f:
        if '<Item class="Part"' in line:
            cap = True
            buf = [line]
            continue
        if cap:
            buf.append(line)
            if '</Item>' in line:
                cap = False
                text = "".join(buf)
                if 'blends_grassoverlays_01_' in text and '<Y>0.0299999993</Y>' in text and '<X>3' in text:
                    print(text[:1200])
                    break

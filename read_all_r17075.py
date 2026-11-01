rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    cap = False
    for line in f:
        if 'referent="R17075"' in line:
            cap = True
        if cap:
            lines.append(line)
            if '</Item>' in line and len(lines) > 50:
                # Part closing item
                if '</Item>' in line and line.strip() == '</Item>' and lines[-2].strip() == '</Properties>':
                    pass
    # find all Texture urls in lines
    import re
    text = "".join(lines[:250])
    urls = re.findall(r'<Content name="Texture"><url>([^<]+)</url></Content>', text)
    zinds = re.findall(r'<int name="ZIndex">([^<]+)</int>', text)
    print(f"URLs: {urls}")
    print(f"ZIndexes: {zinds}")

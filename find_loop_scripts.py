rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

scripts = []
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    buf = []
    cap = False
    name = ""
    for idx, line in enumerate(f):
        if '<Item class="LocalScript"' in line or '<Item class="Script"' in line:
            cap = True
            buf = [line]
            continue
        if cap:
            buf.append(line)
            if '<string name="Name">' in line:
                m = re.search(r'<string name="Name">([^<]+)</string>', line)
                if m:
                    name = m.group(1)
            if '</Item>' in line:
                cap = False
                src = "".join(buf)
                if 'RenderStepped' in src or 'Heartbeat' in src or 'Stepped' in src or 'while' in src:
                    scripts.append((name, src))
                buf = []

print(f"Total loop scripts found: {len(scripts)}")
for n, s in scripts:
    print("  - Script:", n, "length:", len(s))

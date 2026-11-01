rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    buf = []
    cap = False
    for line in f:
        if 'IsometricCamera' in line or 'IsometricController' in line:
            cap = True
            buf = [line]
            continue
        if cap:
            buf.append(line)
            if '</ProtectedString>' in line or '</Item>' in line:
                if len(buf) > 50:
                    print("".join(buf[:80]))
                    print("\n--- MIDDLE ---\n")
                    print("".join(buf[80:160]))
                    break

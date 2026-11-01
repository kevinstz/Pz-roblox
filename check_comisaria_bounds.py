import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_com = False
    depth = 0
    xs, ys, zs = [], [], []
    reading_cf = False
    
    for line in f:
        if '<Item class="Model" referent="R102808">' in line:
            in_com = True
            depth = 1
            continue
        if in_com:
            if '<Item' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    break
            if '<CoordinateFrame name="CFrame">' in line:
                reading_cf = True
                cf_vals = []
                continue
            if reading_cf:
                m = re.search(r'<([XYZ])>([^<]+)</\1>', line)
                if m:
                    cf_vals.append((m.group(1), float(m.group(2))))
                    if len(cf_vals) == 3:
                        d = dict(cf_vals)
                        xs.append(d['X'])
                        ys.append(d['Y'])
                        zs.append(d['Z'])
                        reading_cf = False

print(f"Comisaria parts: {len(xs)}")
print(f"X bounds: [{min(xs):.1f}, {max(xs):.1f}]")
print(f"Y bounds: [{min(ys):.1f}, {max(ys):.1f}]")
print(f"Z bounds: [{min(zs):.1f}, {max(zs):.1f}]")

# Check if player pos (-7.5, 3.0, 112.5) is inside bounds + 2 studs:
px, py, pz = -7.5, 3.0, 112.5
in_x = (min(xs) - 2 <= px <= max(xs) + 2)
in_z = (min(zs) - 2 <= pz <= max(zs) + 2)
print(f"Is player at ({px}, {pz}) inside Comisaria bounds? X={in_x}, Z={in_z}")

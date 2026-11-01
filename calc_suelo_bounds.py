import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_suelo = False
    depth = 0
    xs, ys, zs = [], [], []
    part_count = 0
    reading_cf = False
    
    for line in f:
        if '<Item class="Model" referent="R739">' in line:
            in_suelo = True
            depth = 1
            continue
        if in_suelo:
            if '<Item' in line:
                depth += 1
                if 'class="Part"' in line:
                    part_count += 1
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

print(f"Total parts in Suelo_Piso_0: {part_count}")
print(f"X range: {min(xs)} to {max(xs)} (span: {max(xs)-min(xs):.1f})")
print(f"Y range: {min(ys)} to {max(ys)} (span: {max(ys)-min(ys):.1f})")
print(f"Z range: {min(zs)} to {max(zs)} (span: {max(zs)-min(zs):.1f})")

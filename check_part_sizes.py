import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

sizes = []
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_suelo = False
    in_part = False
    in_size = False
    for line in f:
        if '<Item class="Model" referent="R739">' in line:
            in_suelo = True
            continue
        if in_suelo:
            if '<Vector3 name="size">' in line:
                in_size = True
                s_vals = []
                continue
            if in_size:
                m = re.search(r'<([XYZ])>([^<]+)</\1>', line)
                if m:
                    s_vals.append((m.group(1), float(m.group(2))))
                    if len(s_vals) == 3:
                        d = dict(s_vals)
                        sizes.append((d['X'], d['Y'], d['Z']))
                        in_size = False
            if '<Item class="Model"' in line and 'R739' not in line:
                break

print(f"Total parts in current Suelo_Piso_0: {len(sizes)}")
sx_list = [s[0] for s in sizes]
sz_list = [s[2] for s in sizes]
print(f"Max size X: {max(sx_list)}, max size Z: {max(sz_list)}")
print(f"Parts with size > 50 studs: {sum(1 for s in sizes if s[0] > 50 or s[2] > 50)}")
print(f"Parts with size > 100 studs: {sum(1 for s in sizes if s[0] > 100 or s[2] > 100)}")
print(f"Parts with size > 200 studs: {sum(1 for s in sizes if s[0] > 200 or s[2] > 200)}")

# Find the largest parts:
large = sorted(sizes, key=lambda s: s[0]*s[2], reverse=True)[:10]
for l in large:
    print(f"  Large part: size = ({l[0]:.1f}, {l[1]:.1f}, {l[2]:.1f}), area = {l[0]*l[2]:.0f} sq studs")

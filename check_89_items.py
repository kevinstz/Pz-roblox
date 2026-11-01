src = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

in_suelo0 = False
items = []
current_model = ""

with open(src, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'name="Name">Suelo_Piso_0<' in line:
            in_suelo0 = True
            continue
        elif in_suelo0 and 'name="Name">Suelo_Piso_1<' in line:
            break
        if in_suelo0:
            if '<string name="Name">' in line:
                current_model = line.strip()
            if '<token name="ModelStreamingMode">' in line:
                items.append((i, current_model, line.strip()))

print("Found items:", len(items))
for idx, name, val in items[:10]:
    print(idx, name, val)
print("...")
for idx, name, val in items[-5:]:
    print(idx, name, val)

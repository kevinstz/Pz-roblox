import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Find occurrences of Suelo|roofs_03_54
matches = list(re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">(Suelo\|roofs_03_54)</string>', text, re.DOTALL))
print(f"Found {len(matches)} occurrences of Suelo|roofs_03_54")

for i, m in enumerate(matches[:5]):
    ref = m.group(2)
    s = m.start()
    e = text.find('</Item>', s)
    block = text[s:e+7]
    print(f"\n--- Occurrence {i} (ref: {ref}) ---")
    cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block, re.DOTALL)
    sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
    tex = re.search(r'<url>([^<]+)</url>', block)
    if cf: print("Position:", cf.groups())
    if sz: print("Size:", sz.groups())
    if tex: print("Texture:", tex.group(1))

# Let's see the bounding box of all Suelo|roofs_03_54
xs, ys, zs = [], [], []
for m in matches:
    s = m.start()
    e = text.find('</Item>', s)
    block = text[s:e+7]
    cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block, re.DOTALL)
    if cf:
        xs.append(float(cf.group(1)))
        ys.append(float(cf.group(2)))
        zs.append(float(cf.group(3)))

if xs:
    print(f"\nSuelo|roofs_03_54 Bounding Box: X=[{min(xs):.1f}, {max(xs):.1f}], Y=[{min(ys):.1f}, {max(ys):.1f}], Z=[{min(zs):.1f}, {max(zs):.1f}]")

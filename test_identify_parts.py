import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's collect all referents to remove:
# 1. House 28 old sprite roofs
house_28_refs = [
    'R126859', 'R126877', 'R126889', 'R126892', 'R126895', 'R126898',
    'R126901', 'R126904', 'R126907', 'R126910', 'R126913', 'R126916',
    'R126919', 'R126922', 'R126925', 'R126928', 'R126931', 'R126934',
    'R126937', 'R126940', 'R126943', 'R126946', 'R126949', 'R126952',
    'R126955', 'R126958', 'R126961', 'R126964', 'R126967', 'R126970', 'R126973'
]

# 2. House 22 old sprite roofs
house_22_refs = [
    'R119849', 'R119852', 'R119855', 'R119861', 'R119864', 'R119867',
    'R120169', 'R120193', 'R120553', 'R120556', 'R120559', 'R120565',
    'R120568', 'R120571', 'R120589', 'R120592', 'R120595', 'R120601',
    'R120604', 'R120607', 'R120610', 'R120613', 'R120616'
]

# 3. House 33 old sprite roofs
# Let's dynamically get all roof parts for House 33 in Exterior
h33_matches = []
for ref_m in re.finditer(r'<Item class="([^"]+)" referent="(R\d+)">\s*<Properties>.*?<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text, re.DOTALL):
    cls, r, x, y, z = ref_m.group(1), ref_m.group(2), float(ref_m.group(3)), float(ref_m.group(4)), float(ref_m.group(5))
    if 145 <= x <= 170 and 8 <= z <= 40 and y >= 6.5 and not r.startswith('R200'):
        # check name
        b_end = text.find('</Item>', ref_m.start())
        name_m = re.search(r'<string name="Name">([^<]+)</string>', text[ref_m.start():b_end])
        if name_m and ('roof' in name_m.group(1).lower() or 'wall' in name_m.group(1).lower()):
            if 'exterior_house_02_8' not in name_m.group(1) and 'wooden' not in name_m.group(1) and 'interior' not in name_m.group(1):
                h33_matches.append((r, name_m.group(1), x, y, z))

print(f"House 28 refs found in text: {sum(1 for r in house_28_refs if f'referent=\"{r}\"' in text)} / {len(house_28_refs)}")
print(f"House 22 refs found in text: {sum(1 for r in house_22_refs if f'referent=\"{r}\"' in text)} / {len(house_22_refs)}")
print(f"House 33 sprite roof parts identified: {len(h33_matches)}")
for r in h33_matches[:10]:
    print(f"  {r[0]}: {r[1]} at ({r[2]:.1f}, {r[3]:.1f}, {r[4]:.1f})")

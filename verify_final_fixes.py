import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("File size:", len(text))

# 1. Check Bar_31_45_12 commercial walls
bar_commercial = []
for ref in ['R91073', 'R91522', 'R133577', 'R133562', 'R133849', 'R134152']:
    target = f'referent="{ref}"'
    idx = text.find(target)
    if idx != -1:
        end = text.find('</Item>', idx)
        block = text[idx:end]
        m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
        m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
        m_tex = re.search(r'<url>([^<]+)</url>', block)
        bar_commercial.append((ref, m_name.group(1) if m_name else '?', m_col.group(1) if m_col else '?', m_tex.group(1) if m_tex else '?'))

print("\n1. Sample updated Bar wall panels:")
for r in bar_commercial:
    print(f"  {r[0]}: Name={r[1]}, Col={r[2]}, Tex={r[3]}")

# 2. Check Bar pitched roof
r131081_idx = text.find('referent="R131081"')
if r131081_idx != -1:
    end = text.find('</Item>', r131081_idx)
    block = text[r131081_idx:end]
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    print(f"\n2. Bar Pitched Roof R131081: Pos={m_cf.groups() if m_cf else '?'}, Size={m_sz.groups() if m_sz else '?'}")

# Check removed parts:
removed_samples = ['R133571', 'R133837', 'R133846', 'R126859', 'R126892', 'R119849', 'R120553', 'R137569', 'R140617']
print("\n3. Verifying removed obsolete parts:")
for r in removed_samples:
    present = f'referent="{r}"' in text
    print(f"  {r}: {'PRESENT (ERROR)' if present else 'REMOVED (OK)'}")

# 4. Check protected systems
print("\n4. Checking protected game assets:")
print(f"  Vehiculos folder present: {'name=\"Name\">Vehiculos<' in text}")
print(f"  Character controller present: {'RBXSurvivorCharCtrl' in text}")
print(f"  Isometric cursor present: {'RBXIsoCursorCtrl' in text}")
print(f"  Auto_Sedan present: {'Auto_Sedan' in text}")
print(f"  Auto_Familiar present: {'Auto_Familiar' in text}")
print(f"  Camioneta present: {'Camioneta' in text}")
print(f"  Policia present: {'Policia' in text}")
print(f"  XML tag balance: Open={text.count('<Item ')} vs Close={text.count('</Item>')}")

import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

def get_item_block(text, ref):
    pattern = f'<Item class="[^"]+" referent="{ref}">'
    m = re.search(pattern, text)
    if not m: return None
    s = m.start()
    pos = m.end()
    depth = 1
    while depth > 0 and pos < len(text):
        next_open = text.find('<Item', pos)
        next_close = text.find('</Item>', pos)
        if next_close == -1: break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            pos = next_close + 7
            if depth == 0:
                return text[s:pos]
    return None

# House 33 bounds: X in [145, 170], Z in [8, 40]
# In task-4367, we saw:
# R137443, R137497, R137536, R137563 (roofs_05_39)
# R137569 .. R137640
# R140617 .. R140710
# Let's find all refs in Exterior_8160_11664 and Exterior_8144_11680 that have roof in name and are in House 33:
h33_refs = []
for ref_num in range(137440, 137650):
    ref = f"R{ref_num}"
    b = get_item_block(text, ref)
    if b and 'roof' in b.lower():
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', b, re.DOTALL)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            if 145 <= x <= 170 and 8 <= z <= 40 and y >= 6.5:
                m_name = re.search(r'<string name="Name">([^<]+)</string>', b)
                h33_refs.append((ref, m_name.group(1) if m_name else "Unknown", x, y, z))

for ref_num in range(140600, 140720):
    ref = f"R{ref_num}"
    b = get_item_block(text, ref)
    if b and 'roof' in b.lower():
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', b, re.DOTALL)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            if 145 <= x <= 170 and 8 <= z <= 40 and y >= 6.5:
                m_name = re.search(r'<string name="Name">([^<]+)</string>', b)
                h33_refs.append((ref, m_name.group(1) if m_name else "Unknown", x, y, z))

print(f"House 33 old roof parts found: {len(h33_refs)}")
for r in h33_refs[:5]:
    print(f"  {r[0]}: {r[1]} at ({r[2]:.1f}, {r[3]:.1f}, {r[4]:.1f})")
print("  ...")
for r in h33_refs[-5:]:
    print(f"  {r[0]}: {r[1]} at ({r[2]:.1f}, {r[3]:.1f}, {r[4]:.1f})")

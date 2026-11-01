import json

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

def find_item_bounds_fast(text, ref):
    target = f'referent="{ref}"'
    ref_idx = text.find(target)
    if ref_idx == -1:
        return None, None
    item_start = text.rfind('<Item ', max(0, ref_idx - 500), ref_idx)
    if item_start == -1:
        return None, None
    pos = ref_idx + len(target)
    depth = 1
    while depth > 0 and pos < len(text):
        next_open = text.find('<Item', pos)
        next_close = text.find('</Item>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            pos = next_close + 7
            if depth == 0:
                if pos < len(text) and text[pos] == '\r': pos += 1
                if pos < len(text) and text[pos] == '\n': pos += 1
                return item_start, pos
    return None, None

import re
h33_roof_refs = []
for ref_num in list(range(137440, 137650)) + list(range(140600, 140720)):
    ref = f"R{ref_num}"
    s, e = find_item_bounds_fast(text, ref)
    if s is not None:
        b = text[s:e]
        if 'roof' in b.lower():
            m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', b, re.DOTALL)
            if m_cf:
                x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
                if 145 <= x <= 170 and 8 <= z <= 40 and y >= 6.5:
                    h33_roof_refs.append(ref)

print("H33 roof refs count:", len(h33_roof_refs))
print("H33 roof refs:", h33_roof_refs)
with open("h33_roof_refs.json", "w") as f:
    json.dump(h33_roof_refs, f)

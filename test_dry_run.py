import re

# Test on House 33 refs:
DELETE_REFS = set([
    'R140219', 'R140246', 'R140273', 'R140300', 'R140326', 'R140365',
    'R140482', 'R140494', 'R140587', 'R140590', 'R140593', 'R140596', 'R140599'
])

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

doors_fixed = 0
walls_fixed = 0
roofs_collide_fixed = 0
roof_gaps_closed = 0
deleted_count = 0

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    current_ref = ""

    for line in fin:
        if not buffering:
            if '<Item class="Part"' in line or '<Item class="WedgePart"' in line:
                m_ref = re.search(r'referent="([^"]+)"', line)
                current_ref = m_ref.group(1) if m_ref else ""
                buffering = True
                depth = 1
                buffer = [line]
                continue
        else:
            buffer.append(line)
            if '<Item ' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    buffering = False
                    if current_ref in DELETE_REFS:
                        deleted_count += 1
                        buffer = []
                        continue
                    
                    block = "".join(buffer)
                    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                    if m_name:
                        name = m_name.group(1)
                        if name.startswith('Puerta_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                doors_fixed += 1
                        elif name.startswith('walls_exterior_') or name.startswith('walls_commercial_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                walls_fixed += 1
                        elif name.startswith('roofs_') or name.startswith('Suelo|roofs_') or name.startswith('Suelo|ceilings_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                roofs_collide_fixed += 1
                            m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
                            if m_sz:
                                sx, sy, sz = float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))
                                if (2.85 < sx < 3.0) or (2.85 < sz < 3.0):
                                    roof_gaps_closed += 1
                    buffer = []

print(f"Stats from dry run:")
print(f"  Deleted obsolete House 33 roofs: {deleted_count} / {len(DELETE_REFS)}")
print(f"  Doors to fix CanCollide: {doors_fixed}")
print(f"  Walls to fix CanCollide: {walls_fixed}")
print(f"  Roofs to fix CanCollide: {roofs_collide_fixed}")
print(f"  Roof gaps to close (seams): {roof_gaps_closed}")

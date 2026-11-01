import re

DELETE_REFS = set([
    'R140219', 'R140246', 'R140273', 'R140300', 'R140326', 'R140365',
    'R140482', 'R140494', 'R140587', 'R140590', 'R140593', 'R140596', 'R140599'
])

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

doors_coll_count = 0
walls_coll_count = 0
roofs_coll_count = 0
roof_seams_count = 0
deleted_count = 0
bar_white_count = 0

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    current_ref = ""
    in_bar = False

    for line in fin:
        if '<string name="Name">Bar_31_45_12</string>' in line:
            in_bar = True
        elif in_bar and '<Item class="Model"' in line and depth == 0:
            in_bar = False

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
                                doors_coll_count += 1
                        elif name.startswith('walls_exterior_') or name.startswith('walls_commercial_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                walls_coll_count += 1
                            if in_bar and '684037041b29ec20554a.png' in block:
                                bar_white_count += 1
                        elif 'roof' in name.lower() or 'ceiling' in name.lower() or 'techo' in name.lower():
                            if '<bool name="CanCollide">false</bool>' in block:
                                roofs_coll_count += 1
                            m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
                            if m_sz:
                                sx, sy, sz = float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))
                                if (2.85 < sx < 3.0) or (2.85 < sz < 3.0):
                                    roof_seams_count += 1

                    buffer = []

print("Dry run counts:")
print(f"  Obsolete House 33 roofs deleted: {deleted_count} / {len(DELETE_REFS)}")
print(f"  Doors CanCollide enabled: {doors_coll_count}")
print(f"  Walls CanCollide enabled: {walls_coll_count}")
print(f"  Roofs CanCollide enabled: {roofs_coll_count}")
print(f"  Roof seams expanded (gaps closed): {roof_seams_count}")
print(f"  Bar white wall panels converted to brick: {bar_white_count}")

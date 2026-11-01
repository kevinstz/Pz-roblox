import os
import re
import time

DELETE_REFS = set([
    'R140219', 'R140246', 'R140273', 'R140300', 'R140326', 'R140365',
    'R140482', 'R140494', 'R140587', 'R140590', 'R140593', 'R140596', 'R140599'
])

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
TMP_PATH = r"out\PZ_Rosewood.rbxlx.tmp"

start_time = time.time()

deleted_count = 0
doors_fixed = 0
walls_fixed = 0
roofs_coll_fixed = 0
roof_seams_fixed = 0
white_walls_fixed = 0

def close_roof_seams(block):
    m = re.search(r'(<Vector3 name="size">\s*<X>)([^<]+)(</X>\s*<Y>[^<]+</Y>\s*<Z>)([^<]+)(</Z>)', block)
    if m:
        sx = float(m.group(2))
        sz = float(m.group(4))
        new_sx = 3.02 if 2.85 < sx < 3.0 else sx
        new_sz = 3.02 if 2.85 < sz < 3.0 else sz
        if new_sx != sx or new_sz != sz:
            new_size_tag = f"{m.group(1)}{new_sx:.4f}{m.group(3)}{new_sz:.4f}{m.group(5)}"
            block = block[:m.start()] + new_size_tag + block[m.start() + len(m.group(0)):]
            return block, True
    return block, False

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin, \
     open(TMP_PATH, "w", encoding="utf-8") as fout:

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
            else:
                fout.write(line)
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
                        name_lower = name.lower()

                        # 1. Door collisions
                        if name.startswith('Puerta_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                block = block.replace('<bool name="CanCollide">false</bool>', '<bool name="CanCollide">true</bool>')
                                doors_fixed += 1

                        # 2. Wall collisions & white commercial panels
                        elif name.startswith('walls_exterior_') or name.startswith('walls_commercial_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                block = block.replace('<bool name="CanCollide">false</bool>', '<bool name="CanCollide">true</bool>')
                                walls_fixed += 1
                            if '684037041b29ec20554a.png' in block:
                                block = block.replace('684037041b29ec20554a.png', '519c46ad323a93d7bdf1.png')
                                block = block.replace('4289243802', '4286407990')
                                white_walls_fixed += 1

                        # 3. Roof collisions & seam expansion
                        elif 'roof' in name_lower or 'techo' in name_lower or 'ceiling' in name_lower:
                            if '<bool name="CanCollide">false</bool>' in block:
                                block = block.replace('<bool name="CanCollide">false</bool>', '<bool name="CanCollide">true</bool>')
                                roofs_coll_fixed += 1
                            block, changed = close_roof_seams(block)
                            if changed:
                                roof_seams_fixed += 1

                    fout.write(block)
                    buffer = []

elapsed = time.time() - start_time
print(f"Transformation complete in {elapsed:.2f} seconds.")
print(f"Stats:")
print(f"  Deleted obsolete House 33 roofs: {deleted_count} / {len(DELETE_REFS)}")
print(f"  Doors CanCollide enabled: {doors_fixed}")
print(f"  Walls CanCollide enabled: {walls_fixed}")
print(f"  Roofs CanCollide enabled: {roofs_coll_fixed}")
print(f"  Roof seams closed (expanded): {roof_seams_fixed}")
print(f"  White commercial panels converted to red brick: {white_walls_fixed}")

tmp_size = os.path.getsize(TMP_PATH)
orig_size = os.path.getsize(RBXLX_PATH)
print(f"File sizes: Original = {orig_size:,} bytes, New = {tmp_size:,} bytes")

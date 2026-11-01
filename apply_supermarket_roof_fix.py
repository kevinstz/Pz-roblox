import os
import re
import time

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
TMP_PATH = r"out\PZ_Rosewood.rbxlx.tmp"

start_time = time.time()

ROW_MAPPINGS = {
    -45.0: ('roofs_30_06_3', '78b41ee5804fbd1edad6.png', 'e0c643bc5d88072b2645.png', 4.85, 0.736, 0.297),
    -48.0: ('roofs_30_06_2', '1bdcd7c74292622119e9.png', 'd1d755b0c6f2d4799928.png', 3.22, 0.0, 0.0),
    -51.0: ('roofs_30_06_1', 'e1f8fab0978912f9e2ea.png', '6f951005fc231def8cc5.png', 3.22, 0.0, 0.0),
    -54.0: ('roofs_30_06_0', '61ab6ea868ea59cd888a.png', 'a2c17fce284d60c05645.png', 3.22, 0.0, 0.0),
    -57.0: ('roofs_30_06_5', 'ff458693e881b5dde409.png', '1f46545b44a21fdf0db1.png', 3.22, 0.0, 0.0),
    -60.0: ('roofs_30_06_4', '83cd8684a2a27692226c.png', '241bddcafb699f2560e4.png', 3.22, 0.0, 0.0),
    -63.0: ('roofs_30_06_3', '78b41ee5804fbd1edad6.png', 'e0c643bc5d88072b2645.png', 3.22, 0.0, 0.0),
    -66.0: ('roofs_30_06_2', '1bdcd7c74292622119e9.png', 'd1d755b0c6f2d4799928.png', 3.22, 0.0, 0.0),
}

updated_parts = 0
ridge_hidden = 0

def update_decal_in_block(block, target_face, new_tex):
    pattern = re.compile(r'(<Item class="Decal"[^>]*>.*?</Item>)', re.DOTALL)
    def repl_decal(match):
        decal_text = match.group(1)
        m_face = re.search(r'<token name="Face">(\d+)</token>', decal_text)
        if m_face and m_face.group(1) == str(target_face):
            decal_text = re.sub(
                r'<Content name="Texture"><url>rbxasset://pz42/[^<]+</url></Content>',
                f'<Content name="Texture"><url>rbxasset://pz42/{new_tex}</url></Content>',
                decal_text
            )
        return decal_text
    return pattern.sub(repl_decal, block)

def update_cframe_and_size(block, dz, dy, new_sz_z):
    if dz != 0 or dy != 0:
        m_cf = re.search(r'(<CoordinateFrame name="CFrame">\s*<X>[^<]+</X>\s*<Y>)([^<]+)(</Y>\s*<Z>)([^<]+)(</Z>)', block)
        if m_cf:
            old_y = float(m_cf.group(2))
            old_z = float(m_cf.group(4))
            new_y = old_y + dy
            new_z = old_z + dz
            new_cf = f"{m_cf.group(1)}{new_y:.6f}{m_cf.group(3)}{new_z:.6f}{m_cf.group(5)}"
            block = block[:m_cf.start()] + new_cf + block[m_cf.start() + len(m_cf.group(0)):]
    
    m_sz = re.search(r'(<Vector3 name="size">\s*<X>[^<]+</X>\s*<Y>[^<]+</Y>\s*<Z>)([^<]+)(</Z>)', block)
    if m_sz:
        new_sz_tag = f"{m_sz.group(1)}{new_sz_z:.4f}{m_sz.group(3)}"
        block = block[:m_sz.start()] + new_sz_tag + block[m_sz.start() + len(m_sz.group(0)):]
    
    return block

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin, \
     open(TMP_PATH, "w", encoding="utf-8") as fout:

    buffering = False
    depth = 0
    buffer = []

    for line in fin:
        if not buffering:
            if '<Item class="Part"' in line:
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
                    block = "".join(buffer)
                    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                    if m_name and m_name.group(1).startswith('roofs_30_06_'):
                        pname = m_name.group(1)
                        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?</CoordinateFrame>', block, re.DOTALL)
                        if m_cf:
                            m_z = re.search(r'<Z>([^<]+)</Z>', m_cf.group(0))
                            if m_z:
                                z = float(m_z.group(1))
                                if pname == 'roofs_30_06_100':
                                    # Hide ridge cap billboard fins
                                    block = block.replace('<float name="Transparency">0</float>', '<float name="Transparency">1</float>')
                                    ridge_hidden += 1
                                else:
                                    matched_row = None
                                    for target_z in ROW_MAPPINGS:
                                        if abs(z - target_z) < 1.0:
                                            matched_row = ROW_MAPPINGS[target_z]
                                            break
                                    
                                    if matched_row:
                                        new_name, tex1, tex4, sz_z, dz, dy = matched_row
                                        # 1. Update Name
                                        block = re.sub(r'<string name="Name">roofs_30_06_[^<]+</string>', f'<string name="Name">{new_name}</string>', block)
                                        # 2. Update Color3uint8 to light grey
                                        block = re.sub(r'<Color3uint8 name="Color3uint8">\d+</Color3uint8>', '<Color3uint8 name="Color3uint8">4284505431</Color3uint8>', block)
                                        # 3. Update Decals
                                        block = update_decal_in_block(block, 1, tex1)
                                        block = update_decal_in_block(block, 4, tex4)
                                        # 4. Update CFrame and Size
                                        block = update_cframe_and_size(block, dz, dy, sz_z)
                                        # 5. Ensure CanCollide is true
                                        block = block.replace('<bool name="CanCollide">false</bool>', '<bool name="CanCollide">true</bool>')
                                        updated_parts += 1

                    fout.write(block)
                    buffer = []

elapsed = time.time() - start_time
print(f"Roof transformation complete in {elapsed:.2f} seconds.")
print(f"Stats:")
print(f"  Right slope parts updated: {updated_parts} / 280")
print(f"  Ridge billboard caps hidden: {ridge_hidden} / 35")
print(f"  Original size: {os.path.getsize(RBXLX_PATH):,} bytes")
print(f"  New size:      {os.path.getsize(TMP_PATH):,} bytes")

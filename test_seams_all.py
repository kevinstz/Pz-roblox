import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

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

transformed = 0
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
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
            buffer.append(line)
            if '<Item ' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    buffering = False
                    block = "".join(buffer)
                    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                    if m_name:
                        name = m_name.group(1).lower()
                        if 'roof' in name or 'techo' in name or 'ceiling' in name:
                            new_block, changed = close_roof_seams(block)
                            if changed:
                                transformed += 1
                    buffer = []

print(f"Total roof blocks transformed to close seams: {transformed}")

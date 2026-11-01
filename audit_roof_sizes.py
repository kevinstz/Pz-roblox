import re
from collections import Counter

roof_sizes = Counter()
RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    for line in fin:
        if not buffering:
            if '<Item class="Part"' in line or '<Item class="WedgePart"' in line:
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
                    if m_name and ('roofs_' in m_name.group(1) or 'ceilings_' in m_name.group(1)):
                        m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
                        if m_sz:
                            sx, sy, sz = round(float(m_sz.group(1)), 3), round(float(m_sz.group(2)), 3), round(float(m_sz.group(3)), 3)
                            roof_sizes[(sx, sz)] += 1
                    buffer = []

print("Roof sizes (X, Z):")
for sz, count in roof_sizes.most_common(20):
    print(f"  {sz}: {count}")

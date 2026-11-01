import re
from collections import Counter

roof_coll_false = []
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
                    if m_name:
                        name = m_name.group(1).lower()
                        if any(w in name for w in ['roof', 'techo', 'ceiling']):
                            if '<bool name="CanCollide">false</bool>' in block:
                                roof_coll_false.append(m_name.group(1))
                    buffer = []

print(f"Total roof/ceiling parts with CanCollide=false: {len(roof_coll_false)}")
for name in Counter(roof_coll_false).most_common(20):
    print(" ", name)

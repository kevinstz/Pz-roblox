import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
no_cancollide = 0
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
                    if m_name and (m_name.group(1).startswith('Puerta_') or m_name.group(1).startswith('walls_exterior_')):
                        if 'CanCollide' not in block:
                            no_cancollide += 1
                    buffer = []

print("Parts without CanCollide property:", no_cancollide)

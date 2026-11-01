import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    count = 0
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
                    m_name = re.search(r'<string name="Name">(roofs_30_06_[^<]+)</string>', block)
                    if m_name and count < 3:
                        print("ROOF PART:", m_name.group(1))
                        for l in buffer:
                            if any(k in l for k in ['size', 'CFrame', 'Texture', 'Face', 'CanCollide', 'Transparency']):
                                print("  ", l.strip())
                        count += 1
                    buffer = []

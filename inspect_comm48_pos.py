import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    current_model = ""
    for line in fin:
        if '<Item class="Model"' in line:
            pass
        if '<string name="Name">' in line:
            name = re.search(r'<string name="Name">([^<]+)</string>', line).group(1)
            if 'Exterior_' in name or 'Bar_' in name:
                current_model = name
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
                    if 'walls_commercial_01_48' in block:
                        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?</CoordinateFrame>', block, re.DOTALL)
                        pos = ""
                        if m_cf:
                            cf_text = m_cf.group(0)
                            x = re.search(r'<X>([^<]+)</X>', cf_text)
                            y = re.search(r'<Y>([^<]+)</Y>', cf_text)
                            z = re.search(r'<Z>([^<]+)</Z>', cf_text)
                            if x and y and z:
                                pos = f"({float(x.group(1)):.1f}, {float(y.group(1)):.1f}, {float(z.group(1)):.1f})"
                        print(f"Model: {current_model} | Pos: {pos}")
                    buffer = []

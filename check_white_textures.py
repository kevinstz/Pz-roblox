import re
from collections import Counter

# Check textures on walls
white_wall_candidates = []
RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

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
                    if any(w in block.lower() for w in ['walls_exterior', 'walls_commercial']):
                        # Check texture urls
                        urls = re.findall(r'<url>rbxasset://pz42/([^<]+)</url>', block)
                        for u in urls:
                            # check if 684037041b29ec20554a or 67cf2d4655419cf61751 still exist
                            if u in ['684037041b29ec20554a.png', '67cf2d4655419cf61751.png']:
                                m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                                white_wall_candidates.append((m_name.group(1) if m_name else 'unknown', u))
                    buffer = []

print("Remaining white commercial textures on walls:", len(white_wall_candidates))
for item in white_wall_candidates[:10]:
    print(" ", item)

import re
from collections import Counter

bar_parts = Counter()
bar_textures = Counter()
RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    in_bar = False
    depth = 0
    buffer = []
    buffering = False
    for line in fin:
        if '<Item class="Model"' in line:
            pass
        if '<string name="Name">Bar_31_45_12</string>' in line:
            in_bar = True
        elif in_bar and '<Item class="Model"' in line and depth == 0:
            # left bar
            pass
        
        if in_bar:
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
                            name = m_name.group(1)
                            bar_parts[name] += 1
                            texs = re.findall(r'<url>rbxasset://pz42/([^<]+)</url>', block)
                            for t in texs:
                                bar_textures[(name, t)] += 1
                        buffer = []
                        if len(bar_parts) > 500:
                            break

print("Bar parts count:", len(bar_parts))
print("Sample bar parts:")
for k, v in bar_parts.most_common(15):
    print(f"  {k}: {v}")

print("\nSample bar textures:")
for (name, tex), v in bar_textures.most_common(15):
    print(f"  {name} -> {tex}: {v}")

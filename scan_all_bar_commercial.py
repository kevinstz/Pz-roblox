import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's search all parts in Bar_31_45_12 and exterior blocks
# Specifically in the region X in [-105, -40], Z in [-80, -10]
# That have walls_commercial or pale cyan colors (4284049516, 4284838261, 4289243802, 4284110673, etc.)

matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
suspicious_parts = []

for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        name = m_name.group(1)
        col = m_col.group(1) if m_col else ""
        
        # Check if in Bar area
        if -105 <= x <= -40 and -80 <= z <= -10:
            if 'commercial' in name or '67cf2d4655419cf61751' in str(m_tex) or '37eea404a114289c66e8' in str(m_tex):
                suspicious_parts.append((ref, name, cls, x, y, z, col, m_tex))

print(f"Total commercial/pale parts in Bar area: {len(suspicious_parts)}")
from collections import Counter
print("By name:", Counter([p[1] for p in suspicious_parts]))
for p in suspicious_parts:
    print(f"Ref={p[0]:8s} | Name={p[1]:26s} | Pos=({p[3]:6.2f}, {p[4]:6.2f}, {p[5]:6.2f}) | Col={p[6]:10s} | Tex={p[7]}")

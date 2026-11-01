import re
import numpy as np

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find all parts in Bar_31_45_12:
idx = text.find('<string name="Name">Bar_31_45_12</string>')
item_idx = text.rfind('<Item class="Model"', 0, idx)
# find next model at top level (indentation)
next_model = text.find('</Item>\n\t\t\t\t<Item class="Model"', item_idx)
block = text[item_idx:next_model]

matches = re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', block, re.DOTALL)
pts = []
for m in matches:
    pblock = m.group(2)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', pblock, re.DOTALL)
    if m_cf:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        pts.append((x, y, z))

pts = np.array(pts)
print(f"Bar_31_45_12 parts: {len(pts)}")
print(f"X range: [{pts[:,0].min():.2f} .. {pts[:,0].max():.2f}]")
print(f"Y range: [{pts[:,1].min():.2f} .. {pts[:,1].max():.2f}]")
print(f"Z range: [{pts[:,2].min():.2f} .. {pts[:,2].max():.2f}]")

# Let's check player position in parking lot: (-21, 0, -45) or (-21, 0, -60)
hx = (pts[:,0].max() - pts[:,0].min()) * 0.5 + 2.0
cx = (pts[:,0].max() + pts[:,0].min()) * 0.5
hz = (pts[:,2].max() - pts[:,2].min()) * 0.5 + 2.0
cz = (pts[:,2].max() + pts[:,2].min()) * 0.5
print(f"Center: ({cx:.2f}, {cz:.2f}), HalfSize: ({hx:.2f}, {hz:.2f})")
print(f"Bounds X: [{cx - hx:.2f} .. {cx + hx:.2f}]")
print(f"Bounds Z: [{cz - hz:.2f} .. {cz + hz:.2f}]")

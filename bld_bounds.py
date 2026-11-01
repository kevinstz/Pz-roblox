# Find bounds of Office_31_45_8
with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
idx = text.find('<string name="Name">Office_31_45_8</string>')
start = text.rfind('<Item class="Model"', 0, idx)
# find end of model: next Model or count nesting
cfs = re.findall(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', text[start:start+500000], re.DOTALL)
xs = [float(c[0]) for c in cfs]
ys = [float(c[1]) for c in cfs]
zs = [float(c[2]) for c in cfs]
print(f"Office_31_45_8: {len(cfs)} parts")
print(f"  X in [{min(xs):.1f}, {max(xs):.1f}]")
print(f"  Y in [{min(ys):.1f}, {max(ys):.1f}]")
print(f"  Z in [{min(zs):.1f}, {max(zs):.1f}]")

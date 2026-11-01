with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

for model_name in ['Exterior_8096_11648', 'Exterior_8112_11648', 'Exterior_8112_11632']:
    idx = text.find(f'<string name="Name">{model_name}</string>')
    if idx == -1: continue
    start = text.rfind('<Item class="Model"', 0, idx)
    # Next model
    next_m = text.find('<Item class="Model"', idx)
    block = text[start:next_m] if next_m != -1 else text[start:start+100000]
    
    parts = re.findall(r'<Item class="(Part|WedgePart|CornerWedgePart)" referent="([^"]+)">(.*?)</Item>', block, re.DOTALL)
    print(f"\n=== {model_name}: {len(parts)} parts ===")
    for cls, ref, p_txt in parts:
        m_name = re.search(r'<string name="Name">([^<]+)</string>', p_txt)
        name = m_name.group(1) if m_name else "?"
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', p_txt, re.DOTALL)
        pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else "?"
        # check if it has accent or roof or window
        print(f"  {ref} | {cls:15s} | {name:30s} | pos={pos}")

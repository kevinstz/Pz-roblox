import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

models = ['R39348', 'R40702', 'R41537', 'R42239', 'R47516', 'R53337', 'R69926', 'R70285', 'R77604', 'R77771', 'R93579', 'R102211', 'R102808', 'R108621']

for ref in models:
    idx = text.find(f'referent="{ref}"')
    if idx != -1:
        m_name = re.search(r'<string name="Name">([^<]+)</string>', text[idx:idx+2500])
        # Find WorldPivotData
        m_cf = re.search(r'<OptionalCoordinateFrame name="WorldPivotData">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text[idx:idx+2500], re.DOTALL)
        pos_str = f"({float(m_cf.group(1)):.1f}, {float(m_cf.group(2)):.1f}, {float(m_cf.group(3)):.1f})" if m_cf else "?"
        print(f"Model {ref:8s}: {m_name.group(1) if m_name else 'Unknown':30s} Pivot: {pos_str}")

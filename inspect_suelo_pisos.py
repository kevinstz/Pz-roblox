import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect Suelo_Piso_1, Suelo_Piso_2, etc.
for piso in ['Suelo_Piso_1', 'Suelo_Piso_2', 'Suelo_Piso_3']:
    idx = text.find(f'<string name="Name">{piso}</string>')
    if idx != -1:
        # Find start and end of this model
        item_start = text.rfind('<Item class="Model"', 0, idx)
        next_model = text.find('\n\t\t\t\t<Item class="Model"', idx)
        chunk = text[item_start:next_model]
        
        matches = list(re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', chunk, re.DOTALL))
        print(f"\n{piso}: {len(matches)} parts")
        
        # Check collision and size
        cc_false = 0
        cc_true = 0
        names = []
        for m in matches:
            b = m.group(3)
            m_cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', b)
            m_n = re.search(r'<string name="Name">([^<]+)</string>', b)
            if m_cc and m_cc.group(1) == 'false': cc_false += 1
            else: cc_true += 1
            if m_n: names.append(m_n.group(1))
            
        print(f"  Collision: True={cc_true}, False={cc_false}")
        from collections import Counter
        print(f"  Top part types: {Counter(names).most_common(10)}")

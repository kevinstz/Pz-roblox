import re
from collections import defaultdict

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect each building model in Edificios:
# Banco_31_45_3, Derelict_31_45_5, Chinesekitchen_31_45_4, Cafe_31_45_7, Office_31_45_9,
# Libreria_31_45_23, Livingroom_31_45_28, Office_31_45_8, Derelict_31_45_22, Bar_31_45_12,
# Office_31_45_24, Livingroom_31_45_33, Comisaria_31_45_38, EstacionBomberos_31_45_42.

bld_models = [
    'Banco_31_45_3', 'Derelict_31_45_5', 'Chinesekitchen_31_45_4', 'Cafe_31_45_7', 'Office_31_45_9',
    'Libreria_31_45_23', 'Livingroom_31_45_28', 'Office_31_45_8', 'Derelict_31_45_22', 'Bar_31_45_12',
    'Office_31_45_24', 'Livingroom_31_45_33', 'Comisaria_31_45_38', 'EstacionBomberos_31_45_42'
]

for bname in bld_models:
    idx = text.find(f'<string name="Name">{bname}</string>')
    if idx == -1:
        print(f"{bname}: Not found")
        continue
    # Find start and end of this building item
    item_start = text.rfind('<Item class="Model"', 0, idx)
    # The end is the next top-level Model or end of Edificios
    # Let's count depth
    pos = item_start + 10
    depth = 1
    while depth > 0 and pos < len(text):
        next_open = text.find('<Item', pos)
        next_close = text.find('</Item>', pos)
        if next_close == -1: break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            pos = next_close + 7
    
    bld_chunk = text[item_start:pos]
    # Find all roof parts inside this building
    roof_names = re.findall(r'<string name="Name">(roof[^<]+)</string>', bld_chunk, re.IGNORECASE)
    wedge_roofs = [r for r in roof_names if 'slope' in r or 'gable' in r or 'ridge' in r]
    sprite_roofs = [r for r in roof_names if r not in wedge_roofs and 'ceiling' not in r and 'antenna' not in r]
    print(f"\nBuilding: {bname}")
    print(f"  3D Wedge roof parts: {len(wedge_roofs)}")
    print(f"  Old Sprite roof parts: {len(sprite_roofs)}")
    if sprite_roofs:
        from collections import Counter
        print(f"  Sprite roof types: {dict(Counter(sprite_roofs))}")

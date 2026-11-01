# Let's check Livingroom_31_45_28 in PZ_Rosewood.rbxlx
# Did apply_house_upgrades remove the original roof parts, or did it just add on top?
import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find Livingroom_31_45_28
idx = text.find('Livingroom_31_45_28')
print("Livingroom_31_45_28 found:", idx != -1)
if idx != -1:
    end = text.find('</Item>', text.find('</Item>', idx) + 1)
    # Find all children models in Livingroom_31_45_28:
    model_block = text[idx:idx+150000]
    piso_models = re.findall(r'<string name="Name">(Piso_[^<]+)</string>', model_block)
    print("Piso models in house 28:", piso_models)
    
    # Check parts in Piso_1:
    piso1_idx = model_block.find('Piso_1')
    piso1_end = model_block.find('</Item>\n\t\t\t\t<Item', piso1_idx)
    piso1_block = model_block[piso1_idx:piso1_idx+50000]
    p1_parts = re.findall(r'<string name="Name">([^<]+)</string>', piso1_block)
    print("Piso_1 parts in house 28 count:", len(p1_parts))
    print("Sample parts:", p1_parts[:15])

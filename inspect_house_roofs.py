import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's see what parts have "roof" in their name or what parts are under Piso_1
# Let's inspect the 3 models named "Piso_1" found earlier:
# Model: Piso_1 (ref: R200036)
# Model: Piso_1 (ref: R200157)
# Model: Piso_1 (ref: R200099)
for m_ref in ['R200036', 'R200157', 'R200099']:
    idx = text.find(f'referent="{m_ref}"')
    if idx != -1:
        end = text.find('</Item>', idx)
        # Find next Item end at same level or just grab the next 3000 chars
        print(f"=== Model Piso_1 ({m_ref}) ===")
        # let's see how many parts are inside this model
        model_chunk = text[idx:idx+20000]
        # find parts inside
        parts = re.findall(r'<string name="Name">([^<]+)</string>', model_chunk)
        print("First 20 names inside:", parts[:20])

# Now let's check what other roofs exist in the entire file!
# Where are all the roofs located?
all_roofs = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]*roof[^<]*)</string>', text, re.DOTALL)
roof_list = []
for m in all_roofs:
    cls, ref, name = m.groups()
    roof_list.append((ref, name, cls))

print(f"\nTotal items with 'roof' in Name: {len(roof_list)}")
from collections import Counter
print("Top 30 roof names:")
for name, cnt in Counter([r[1] for r in roof_list]).most_common(30):
    print(f"  {name}: {cnt}")

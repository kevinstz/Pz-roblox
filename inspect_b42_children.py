import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

r2_idx = text.find('referent="R2"')
props_end = text.find('</Properties>', r2_idx)

# Children of R2 are indented with \t\t\t<Item class="([^"]+)" referent="([^"]+)">
children = re.finditer(r'\n\t\t\t<Item class="([^"]+)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>', text[props_end:props_end+50000], re.DOTALL)

print("Top-level children inside PZ_Rosewood_B42:")
for m in children:
    cls, ref, name = m.groups()
    print(f"  {cls}: {name} (ref: {ref})")

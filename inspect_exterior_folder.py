import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('referent="R116275"')
end_idx = text.find('referent="R153240"')
chunk = text[idx:end_idx]

# Find direct child models inside Exterior
matches = re.finditer(r'\n\t\t\t\t<Item class="([^"]+)" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>', chunk, re.DOTALL)

print("Direct children inside Exterior (R116275):")
for m in matches:
    cls, ref, name = m.groups()
    print(f"  {cls}: {name} (ref: {ref})")

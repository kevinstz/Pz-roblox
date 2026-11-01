import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("File size:", len(text))

# Find models
models = re.findall(r'<Item class="Model" referent="([^"]+)">\s*<Properties>\s*<string name="Name">([^<]+)</string>', text)
print(f"Total models: {len(models)}")
for ref, name in models:
    if any(k in name.lower() for k in ['house', 'living', 'bar', 'exterior', 'roof', 'piso', 'shop', 'station', 'motel']):
        print(f"Model: {name} (ref: {ref})")

# Look for roof items
roof_names = set(re.findall(r'<string name="Name">(roof[s]?_[^<]+)</string>', text, re.IGNORECASE))
print("\nUnique roof part names:")
for r in sorted(roof_names):
    count = text.count(f'<string name="Name">{r}</string>')
    print(f"  {r}: {count}")

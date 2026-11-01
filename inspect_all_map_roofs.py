import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's find all models inside Edificios or everywhere that are residential or buildings
models = re.findall(r'<Item class="Model" referent="([^"]+)">\s*<Properties>.*?<string name="Name">([^<]+)</string>', text, re.DOTALL)
print(f"Total models in file: {len(models)}")
for ref, name in models:
    print(f"  {ref:8s}: {name}")

# Also let's check all roofs across the entire map:
# How many total roof parts exist in the map right now?
roof_matches = re.findall(r'<string name="Name">(roof[s]?_[^<]+)</string>', text, re.IGNORECASE)
print(f"\nTotal roof parts in map: {len(roof_matches)}")
from collections import Counter
print("Top 20 roof part types:")
for k, v in Counter(roof_matches).most_common(20):
    print(f"  {k:30s}: {v}")

import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's find all models or groups that represent buildings or houses
# In Roblox XML:
# <Item class="Model" referent="...">
#   <Properties>
#     <string name="Name">...</string>
models = re.findall(r'<Item class="Model" referent="([^"]+)">\s*<Properties>\s*<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>.*?</CoordinateFrame>\s*<string name="Name">([^<]+)</string>', text, re.DOTALL)
print(f"Total models with CFrame: {len(models)}")
for ref, x, y, z, name in models:
    print(f"  Model: {name:30s} at ({float(x):6.1f}, {float(y):6.1f}, {float(z):6.1f}) [ref: {ref}]")

# Also find models where Name is before CFrame
models2 = re.findall(r'<Item class="Model" referent="([^"]+)">\s*<Properties>\s*<string name="Name">([^<]+)</string>', text)
print(f"\nAll models total: {len(models2)}")
for ref, name in models2:
    print(f"  Model: {name:30s} [ref: {ref}]")

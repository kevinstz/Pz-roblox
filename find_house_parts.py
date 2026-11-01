import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find all models named 'Livingroom...' or 'House...' or 'Exterior...'
models = re.findall(r'<Item class="Model"[^>]*>.*?<string name="Name">([^<]+)</string>', text, re.DOTALL)
print(f"Total models: {len(models)}")
house_models = [m for m in models if 'house' in m.lower() or 'livingroom' in m.lower()]
print(f"House models: {house_models}")

# Where are the gabled roofs from apply_house_upgrades?
# In apply_house_upgrades, parts were named 'roofs_slope_west', 'roofs_slope_east', etc.
print("roofs_slope_west in text:", 'roofs_slope_west' in text)
print("roofs_ridge_cap in text:", 'roofs_ridge_cap' in text)
print("porch_deck in text:", 'porch_deck' in text)
print("skirting_west in text:", 'skirting_west' in text)

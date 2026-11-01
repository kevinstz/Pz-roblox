import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Find items directly under Workspace (indented with \t\t<Item)
# Note: Workspace properties end with </Properties>
ws_idx = text.find('<Item class="Workspace"')
props_end = text.find('</Properties>', ws_idx)

# Search for direct children: \n\t\t<Item class="([^"]+)" referent="([^"]+)">
children = re.findall(r'\n\t\t<Item class="([^"]+)" referent="([^"]+)">', text[props_end:])
print(f"Direct children of Workspace: {len(children)}")
for cls, ref in children[:30]:
    # find Name
    item_idx = text.find(f'referent="{ref}"')
    name_m = re.search(r'<string name="Name">([^<]+)</string>', text[item_idx:item_idx+500])
    name = name_m.group(1) if name_m else "Unknown"
    print(f"  {cls}: {name} (ref: {ref})")

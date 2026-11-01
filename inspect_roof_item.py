import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect the block around roofs_04_48
idx = text.find('roofs_04_48')
# Find the start of Item
item_start = text.rfind('<Item class=', 0, idx)
item_end = text.find('</Item>', idx)
# And let's find the parent Item
parent_start = text.rfind('<Item class=', 0, item_start)
parent_props = text[parent_start:item_start]
m_pname = re.search(r'<string name="Name">([^<]+)</string>', parent_props)

print("Parent name:", m_pname.group(1) if m_pname else "None")
print("\nItem XML:")
print(text[item_start:item_end+7])

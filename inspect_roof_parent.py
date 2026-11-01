with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('Pos=(180.0, 8.1, -245.9)')
# Or find roofs_30_07_29
target = '<string name="Name">roofs_30_07_29</string>'
idx = text.find(target)
print("Found roofs_30_07_29 at", idx)
if idx != -1:
    # Let's find enclosing model/folder
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    # Find parent Item
    parent_start = text.rfind('<Item class="', 0, item_start - 10)
    print("Parent item header:")
    print(text[parent_start:parent_start+300])

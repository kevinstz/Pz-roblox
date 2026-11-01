import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

folders = re.findall(r'<Item class="Folder" referent="([^"]+)">\s*<Properties>\s*<string name="Name">([^<]+)</string>', text)
print(f"Total folders: {len(folders)}")
for ref, name in folders:
    print(f"  Folder: {name} (ref: {ref})")

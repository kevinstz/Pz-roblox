import os
import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

print("Scanning for models and folders in Workspace...")
models = []
in_item = False
curr_item = []

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<Item class="Folder"' in line or '<Item class="Model"' in line:
            in_item = True
            curr_item = [line]
        elif in_item:
            curr_item.append(line)
            if '<string name="Name">' in line:
                m = re.search(r'<string name="Name">(.*?)</string>', line)
                if m:
                    name = m.group(1)
                    models.append((curr_item[0].strip(), name))
                if len(curr_item) > 10:
                    in_item = False
            elif '</Item>' in line:
                in_item = False

print(f"Total Folders/Models found at top levels: {len(models)}")
for cls, name in models[:50]:
    print(f"  {cls} -> {name}")

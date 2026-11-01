import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

ws_idx = text.find('<Item class="Workspace"')
if ws_idx == -1:
    print("No Workspace item?")
else:
    print("Found Workspace at", ws_idx)
    # find direct children: they will have a specific indentation
    # Let's inspect the next 5000 characters
    print(text[ws_idx:ws_idx+3000])

import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('class="SpawnLocation"')
if idx != -1:
    end = text.find('</Item>', idx)
    print(text[idx:end+7])

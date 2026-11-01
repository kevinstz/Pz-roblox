import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('referent="R133580"')
end = text.find('</Item>', idx)
block = text[idx:end+7]
print(block)

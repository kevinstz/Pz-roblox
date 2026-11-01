with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('referent="R133837"')
end = text.find('</Item>', text.find('<Item class="Decal"', idx))
print(text[idx:end+7])

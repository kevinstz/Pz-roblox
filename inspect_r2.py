with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('referent="R2"')
print("Found R2:", idx)
print(text[idx+500:idx+1500])

from test_item_bounds import find_item_bounds

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

s, e = find_item_bounds(text, 'R133861')
block = text[s:e]
print("=== BEFORE R133861 ===")
print("First 200 chars:")
print(block[:200])
print("...")
print("Decal part:")
d_idx = block.find('<Item class="Decal"')
print(block[d_idx:d_idx+300])

new_block = block.replace('<string name="Name">walls_commercial_01_16</string>', '<string name="Name">walls_exterior_house_02_36</string>')
new_block = new_block.replace('<Color3uint8 name="Color3uint8">4284049516</Color3uint8>', '<Color3uint8 name="Color3uint8">4286407990</Color3uint8>')
new_block = new_block.replace('<url>rbxasset://pz42/67cf2d4655419cf61751.png</url>', '<url>rbxasset://pz42/519c46ad323a93d7bdf1.png</url>')

print("\n=== AFTER R133861 ===")
print(new_block[:200])
print("...")
d_idx2 = new_block.find('<Item class="Decal"')
print(new_block[d_idx2:d_idx2+300])

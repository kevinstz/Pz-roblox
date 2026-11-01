with open(r'C:\Users\julia\Downloads\pz_roblox_b42\build_map.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== is_floor_layer definition (lines 90-140) ===")
for i in range(85, 140):
    if i < len(lines):
        print(f"{i+1:4d}: {lines[i]}", end='')

print("\n=== floor generation (lines 500-580) ===")
for i in range(495, 580):
    if i < len(lines):
        print(f"{i+1:4d}: {lines[i]}", end='')

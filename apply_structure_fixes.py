import os
import shutil
import re
import xml.etree.ElementTree as ET

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
BACKUP_PATH = r"out\PZ_Rosewood.rbxlx.bak_structure_fix"
TMP_PATH = r"out\PZ_Rosewood.rbxlx.tmp"

# 1. Parts to remove (12 parts total)
REMOVE_REFS = [
    # Defect 1: Floating white arch pediment on building corner
    'R133864',
    # Defect 3: Jagged roof fin (rotated 64 deg) & floating triangular roof decal
    'R133580',
    'R133855',
    # Defect 4: Protruding wooden rafters through 2nd floor windows across the street
    'R131872', 'R131875', 'R131878', 'R131881', 'R131884', 'R131887', 'R131890',
    'R131841', 'R131858'
]

# 2. Parts to update to brick (32 parts total)
UPDATE_EAST_REFS = [
    # Parapet and upper wall panels along X = -46.39 in Exterior_8080_11648
    'R133861', 'R133876', 'R133882', 'R133891', 'R133897',
    'R133912', 'R133918', 'R133924', 'R133930', 'R133936', 'R133951', 'R133957',
    'R133963', 'R133966', 'R133969', 'R133987', 'R133990',
    'R134002', 'R134005', 'R134008', 'R134026', 'R134029', 'R134041', 'R134044',
    # Upper facade panels in Exterior_8080_11664
    'R136287', 'R136293', 'R136299',
    'R136419', 'R136422', 'R136425'
]

UPDATE_SOUTH_REFS = [
    # South-facing upper wall panels at Z = -67.32 in Exterior_8080_11648
    'R133852', 'R133858'
]

def find_item_bounds(text, ref):
    pattern = f'<Item class="[^"]+" referent="{ref}">'
    m = re.search(pattern, text)
    if not m:
        return None, None
    start = m.start()
    
    pos = m.end()
    depth = 1
    while depth > 0 and pos < len(text):
        next_open = text.find('<Item', pos)
        next_close = text.find('</Item>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            pos = next_close + 7
            if depth == 0:
                if pos < len(text) and text[pos] == '\r': pos += 1
                if pos < len(text) and text[pos] == '\n': pos += 1
                return start, pos
    return None, None

def main():
    print("=== STARTING STRUCTURAL FIXES ===")
    
    # Step 1: Backup
    if not os.path.exists(BACKUP_PATH):
        print(f"Creating safety backup: {BACKUP_PATH}...")
        shutil.copy2(RBXLX_PATH, BACKUP_PATH)
        print("Backup created successfully.")
    else:
        print(f"Backup already exists: {BACKUP_PATH}")

    # Step 2: Read file
    print("Reading file content...")
    with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    orig_len = len(text)
    print(f"Original file length: {orig_len} chars")

    # Step 3: Update Defect 2 parts in-place
    print("\n--- Applying Fix 2: Parapet & Upper Wall Panels to Solid Brick ---")
    update_count = 0
    for ref in UPDATE_EAST_REFS:
        s, e = find_item_bounds(text, ref)
        if s is None:
            print(f"WARNING: Referent {ref} not found for update!")
            continue
        block = text[s:e]
        new_block = block.replace('<string name="Name">walls_commercial_01_16</string>',
                                  '<string name="Name">walls_exterior_house_02_36</string>')
        new_block = new_block.replace('<Color3uint8 name="Color3uint8">4284049516</Color3uint8>',
                                      '<Color3uint8 name="Color3uint8">4286407990</Color3uint8>')
        new_block = new_block.replace('<url>rbxasset://pz42/67cf2d4655419cf61751.png</url>',
                                      '<url>rbxasset://pz42/519c46ad323a93d7bdf1.png</url>')
        text = text[:s] + new_block + text[e:]
        update_count += 1
    print(f"Updated {update_count} east-facing commercial panels to brick.")

    update_south_count = 0
    for ref in UPDATE_SOUTH_REFS:
        s, e = find_item_bounds(text, ref)
        if s is None:
            print(f"WARNING: Referent {ref} not found for south update!")
            continue
        block = text[s:e]
        new_block = block.replace('<string name="Name">walls_commercial_01_17</string>',
                                  '<string name="Name">walls_exterior_house_02_37</string>')
        new_block = new_block.replace('<Color3uint8 name="Color3uint8">4284838261</Color3uint8>',
                                      '<Color3uint8 name="Color3uint8">4288248651</Color3uint8>')
        new_block = new_block.replace('<url>rbxasset://pz42/37eea404a114289c66e8.png</url>',
                                      '<url>rbxasset://pz42/a25c988cc7b63df67e25.png</url>')
        text = text[:s] + new_block + text[e:]
        update_south_count += 1
    print(f"Updated {update_south_count} south-facing commercial panels to brick.")

    # Step 4: Remove Defect 1, Defect 3, Defect 4 parts
    print("\n--- Applying Fixes 1, 3, 4: Removing 12 Defective Structural Parts ---")
    remove_ranges = []
    for ref in REMOVE_REFS:
        s, e = find_item_bounds(text, ref)
        if s is None:
            print(f"WARNING: Referent {ref} not found for removal!")
            continue
        remove_ranges.append((s, e, ref))
    
    # Sort in descending order of start position so deletions don't invalidate subsequent offsets
    remove_ranges.sort(key=lambda x: x[0], reverse=True)
    
    print(f"Found {len(remove_ranges)} items to remove. Deleting in reverse order...")
    for s, e, ref in remove_ranges:
        print(f"  Removing {ref} (bytes {s}..{e}, len {e-s})")
        text = text[:s] + text[e:]
    
    print(f"Deletions complete. New file length: {len(text)} chars (delta: {len(text) - orig_len} chars)")

    # Step 5: Write to temporary file
    print(f"\nWriting to {TMP_PATH}...")
    with open(TMP_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    
    # Step 6: Atomic replace
    print(f"Replacing {RBXLX_PATH} with updated file...")
    shutil.move(TMP_PATH, RBXLX_PATH)
    print("Replace successful!")

if __name__ == "__main__":
    main()

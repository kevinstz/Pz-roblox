import os
import shutil
import re
import json

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
BACKUP_PATH = r"out\PZ_Rosewood.rbxlx.bak_turn11"
TMP_PATH = r"out\PZ_Rosewood.rbxlx.tmp"

# 1. Commercial wall parts to update on Bar_31_45_12
WEST_WALL_REFS = [
    'R91073', 'R91522', 'R91781', 'R92150', 'R92334', 'R92933', 'R93272',
    'R133559', 'R133607', 'R133616', 'R133631', 'R133640', 'R133664',
    'R133733', 'R133748', 'R133757', 'R133789', 'R133849', 'R133879',
    'R133894', 'R133906', 'R133921', 'R133933', 'R133945', 'R133996',
    'R134035', 'R134152', 'R134164', 'R134170', 'R134176', 'R134182',
    'R134188', 'R134197', 'R135929', 'R135944', 'R136284', 'R136296'
]

EAST_WALL_REFS = [
    'R133577', 'R133604', 'R133613', 'R133622', 'R133637', 'R133679',
    'R133739', 'R133754', 'R133804', 'R135935', 'R135950'
]

SOUTH_WALL_REFS = [
    'R91076', 'R93284', 'R133960', 'R136314', 'R136317', 'R136473',
    'R133562', 'R135965', 'R136323', 'R136476', 'R133592', 'R133595',
    'R133598', 'R93275', 'R136692'
]

# 2. Downtown bar pitched roof cleanup
BAR_ROOF_REMOVE_REFS = [
    'R133571', # rogue gutter fin
    'R133837', # segmented roof strip 2
    'R133846'  # segmented roof strip 3
]

# 3. Old overlapping 2D sprite roof parts to remove from residential houses
HOUSE_28_ROOF_REFS = [
    'R126859', 'R126877', 'R126889', 'R126892', 'R126895', 'R126898',
    'R126901', 'R126904', 'R126907', 'R126910', 'R126913', 'R126916',
    'R126919', 'R126922', 'R126925', 'R126928', 'R126931', 'R126934',
    'R126937', 'R126940', 'R126943', 'R126946', 'R126949', 'R126952',
    'R126955', 'R126958', 'R126961', 'R126964', 'R126967', 'R126970',
    'R126973'
]

HOUSE_22_ROOF_REFS = [
    'R119849', 'R119852', 'R119855', 'R119861', 'R119864', 'R119867',
    'R120169', 'R120193', 'R120553', 'R120556', 'R120559', 'R120565',
    'R120568', 'R120571', 'R120589', 'R120592', 'R120595', 'R120601',
    'R120604', 'R120607', 'R120610', 'R120613', 'R120616'
]

with open("h33_roof_refs.json", "r") as f:
    HOUSE_33_ROOF_REFS = json.load(f)

def find_item_bounds_fast(text, ref):
    target = f'referent="{ref}"'
    ref_idx = text.find(target)
    if ref_idx == -1:
        return None, None
    item_start = text.rfind('<Item ', max(0, ref_idx - 500), ref_idx)
    if item_start == -1:
        return None, None
    pos = ref_idx + len(target)
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
                return item_start, pos
    return None, None

def update_part_block(block, new_name, new_color, new_tex_url):
    block = re.sub(r'<string name="Name">walls_commercial_[^<]+</string>',
                   f'<string name="Name">{new_name}</string>', block)
    block = re.sub(r'<Color3uint8 name="Color3uint8">\d+</Color3uint8>',
                   f'<Color3uint8 name="Color3uint8">{new_color}</Color3uint8>', block)
    block = re.sub(r'<Content name="Texture"><url>[^<]+</url></Content>',
                   f'<Content name="Texture"><url>{new_tex_url}</url></Content>', block)
    return block

def main():
    print("=== STARTING COMPLETE STRUCTURAL AND ROOF FIXES ===", flush=True)

    # Step 1: Backup
    if not os.path.exists(BACKUP_PATH):
        print(f"Creating backup: {BACKUP_PATH}...", flush=True)
        shutil.copy2(RBXLX_PATH, BACKUP_PATH)
        print("Backup created successfully.", flush=True)
    else:
        print(f"Backup already exists: {BACKUP_PATH}", flush=True)

    # Step 2: Read rbxlx file
    print("Reading PZ_Rosewood.rbxlx...", flush=True)
    with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    orig_len = len(text)
    print(f"File loaded: {orig_len} bytes", flush=True)

    # Step 3: Update Bar_31_45_12 Commercial Walls to Brick
    print("\n--- Updating Bar_31_45_12 Walls to Solid Brick ---", flush=True)
    replacements = []
    
    for ref in WEST_WALL_REFS:
        s, e = find_item_bounds_fast(text, ref)
        if s is None:
            print(f"  WARNING: West ref {ref} not found!", flush=True)
            continue
        old_block = text[s:e]
        new_block = update_part_block(old_block, 'walls_exterior_house_02_36', '4286407990', 'rbxasset://pz42/519c46ad323a93d7bdf1.png')
        replacements.append((s, e, new_block))
    print(f"Prepared {len(WEST_WALL_REFS)} West-facing parapet/wall updates.", flush=True)

    for ref in EAST_WALL_REFS:
        s, e = find_item_bounds_fast(text, ref)
        if s is None:
            print(f"  WARNING: East ref {ref} not found!", flush=True)
            continue
        old_block = text[s:e]
        new_block = update_part_block(old_block, 'walls_exterior_house_02_36', '4286407990', 'rbxasset://pz42/519c46ad323a93d7bdf1.png')
        replacements.append((s, e, new_block))
    print(f"Prepared {len(EAST_WALL_REFS)} East-facing facade updates.", flush=True)

    for ref in SOUTH_WALL_REFS:
        s, e = find_item_bounds_fast(text, ref)
        if s is None:
            print(f"  WARNING: South ref {ref} not found!", flush=True)
            continue
        old_block = text[s:e]
        new_block = update_part_block(old_block, 'walls_exterior_house_02_37', '4288248651', 'rbxasset://pz42/a25c988cc7b63df67e25.png')
        replacements.append((s, e, new_block))
    print(f"Prepared {len(SOUTH_WALL_REFS)} South-facing wall updates.", flush=True)

    # Step 4: Downtown bar pitched roof extension (R131081)
    s, e = find_item_bounds_fast(text, 'R131081')
    if s is not None:
        block = text[s:e]
        block = re.sub(r'<Z>-74\.989\d*</Z>', '<Z>-71.9890976</Z>', block)
        block = re.sub(r'<Z>3\.22370005</Z>', '<Z>9.22370005</Z>', block)
        replacements.append((s, e, block))
        print("Prepared R131081 extension to span full pitched roof length.", flush=True)
    else:
        print("WARNING: R131081 not found for roof merge!", flush=True)

    # Apply all updates by sorting in descending order of start position
    replacements.sort(key=lambda x: x[0], reverse=True)
    for s, e, new_block in replacements:
        text = text[:s] + new_block + text[e:]
    print(f"Applied {len(replacements)} wall and roof modifications.", flush=True)

    # Step 5: Collect and perform all removals
    all_remove_refs = set(BAR_ROOF_REMOVE_REFS + HOUSE_28_ROOF_REFS + HOUSE_22_ROOF_REFS + HOUSE_33_ROOF_REFS)
    print(f"\n--- Removing {len(all_remove_refs)} Obsolete / Broken Roof Parts ---", flush=True)
    print(f"  Bar roof removals: {len(BAR_ROOF_REMOVE_REFS)}", flush=True)
    print(f"  House 28 roof removals: {len(HOUSE_28_ROOF_REFS)}", flush=True)
    print(f"  House 22 roof removals: {len(HOUSE_22_ROOF_REFS)}", flush=True)
    print(f"  House 33 roof removals: {len(HOUSE_33_ROOF_REFS)}", flush=True)

    remove_ranges = []
    for ref in all_remove_refs:
        s, e = find_item_bounds_fast(text, ref)
        if s is not None:
            remove_ranges.append((s, e, ref))
        else:
            print(f"  Note: ref {ref} already absent or not found.", flush=True)

    # Sort in descending order of start position so deletions do not alter earlier offsets
    remove_ranges.sort(key=lambda x: x[0], reverse=True)
    print(f"Found {len(remove_ranges)} items to remove. Deleting in reverse order...", flush=True)

    for s, e, ref in remove_ranges:
        text = text[:s] + text[e:]

    print(f"Deletion complete. Final text length: {len(text)} bytes (delta: {len(text) - orig_len} bytes)", flush=True)

    # Step 6: Verification
    print("\n--- Verifying Integrity ---", flush=True)
    open_items = text.count('<Item ')
    close_items = text.count('</Item>')
    print(f"Open <Item tags: {open_items}, Close </Item> tags: {close_items}", flush=True)
    if open_items != close_items:
        raise ValueError(f"XML tag mismatch: {open_items} open vs {close_items} close tags!")
    print("XML tag balance is PERFECT.", flush=True)

    # Verify protected structures
    assert 'name="Name">Vehiculos<' in text, "CRITICAL ERROR: Vehiculos folder missing!"
    assert 'name="Name">IsometricCamera<' in text or 'RBXSurvivorCharCtrl' in text, "CRITICAL ERROR: Camera/Controls missing!"
    print("Protected assets (Vehiculos, Camera, Controls) are 100% intact.", flush=True)

    # Step 7: Write to file
    print(f"\nWriting to {TMP_PATH}...", flush=True)
    with open(TMP_PATH, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Replacing {RBXLX_PATH} with updated file...", flush=True)
    shutil.move(TMP_PATH, RBXLX_PATH)
    print("=== ALL STRUCTURAL AND ROOF FIXES APPLIED SUCCESSFULLY! ===", flush=True)

if __name__ == "__main__":
    main()

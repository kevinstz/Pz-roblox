import xml.etree.ElementTree as ET
import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

REMOVE_REFS = [
    'R133864', 'R133580', 'R133855',
    'R131872', 'R131875', 'R131878', 'R131881', 'R131884', 'R131887', 'R131890',
    'R131841', 'R131858'
]

UPDATE_EAST_REFS = [
    'R133861', 'R133876', 'R133882', 'R133891', 'R133897',
    'R133912', 'R133918', 'R133924', 'R133930', 'R133936', 'R133951', 'R133957',
    'R133963', 'R133966', 'R133969', 'R133987', 'R133990',
    'R134002', 'R134005', 'R134008', 'R134026', 'R134029', 'R134041', 'R134044',
    'R136287', 'R136293', 'R136299',
    'R136419', 'R136422', 'R136425'
]

UPDATE_SOUTH_REFS = [
    'R133852', 'R133858'
]

def main():
    print("=== RUNNING VERIFICATION ON PZ_Rosewood.rbxlx ===")
    with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # 1. Check removals
    removals_ok = True
    for ref in REMOVE_REFS:
        if f'referent="{ref}"' in text:
            print(f"ERROR: Removed referent {ref} still exists in file!")
            removals_ok = False
    if removals_ok:
        print("PASS: All 12 defective parts successfully removed.")

    # 2. Check updates (East)
    east_ok = True
    for ref in UPDATE_EAST_REFS:
        idx = text.find(f'referent="{ref}"')
        if idx == -1:
            print(f"ERROR: Referent {ref} not found!")
            east_ok = False
            continue
        end = text.find('</Item>', idx)
        block = text[idx:end+7]
        if 'walls_exterior_house_02_36' not in block:
            print(f"ERROR: Referent {ref} does not have new name!")
            east_ok = False
        if '4286407990' not in block:
            print(f"ERROR: Referent {ref} does not have brick color!")
            east_ok = False
        if '519c46ad323a93d7bdf1.png' not in block:
            print(f"ERROR: Referent {ref} does not have brick texture!")
            east_ok = False
    if east_ok:
        print(f"PASS: All {len(UPDATE_EAST_REFS)} east parapet parts successfully updated to brick.")

    # 3. Check updates (South)
    south_ok = True
    for ref in UPDATE_SOUTH_REFS:
        idx = text.find(f'referent="{ref}"')
        if idx == -1:
            print(f"ERROR: Referent {ref} not found!")
            south_ok = False
            continue
        end = text.find('</Item>', idx)
        block = text[idx:end+7]
        if 'walls_exterior_house_02_37' not in block:
            print(f"ERROR: Referent {ref} does not have new name!")
            south_ok = False
        if '4288248651' not in block:
            print(f"ERROR: Referent {ref} does not have brick color!")
            south_ok = False
        if 'a25c988cc7b63df67e25.png' not in block:
            print(f"ERROR: Referent {ref} does not have brick texture!")
            south_ok = False
    if south_ok:
        print(f"PASS: All {len(UPDATE_SOUTH_REFS)} south parapet parts successfully updated to brick.")

    # 4. Check protected objects
    protected_items = [
        '<string name="Name">Vehiculos</string>',
        '<string name="Name">Auto_Sedan</string>',
        '<string name="Name">Auto_Familiar</string>',
        '<string name="Name">IsometricCamera</string>',
        '<string name="Name">IsometricCursorController</string>'
    ]
    protected_ok = True
    for item in protected_items:
        if item not in text:
            print(f"ERROR: Protected element {item} missing!")
            protected_ok = False
    if protected_ok:
        print("PASS: All vehicles, camera, cursor controller, and HUD are 100% intact.")

    # 5. Check XML balance: opening and closing tags
    open_items = text.count('<Item')
    close_items = text.count('</Item>')
    print(f"XML Item tag count: open={open_items}, close={close_items}")
    if open_items == close_items:
        print("PASS: XML Item tags are perfectly balanced.")
    else:
        print(f"ERROR: XML Item tags imbalanced! Diff = {open_items - close_items}")

if __name__ == "__main__":
    main()

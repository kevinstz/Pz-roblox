import re
import sys

TARGET = r"out\PZ_Rosewood.rbxlx"

item_open = 0
item_close = 0
doors_false = 0
walls_false = 0
roofs_false = 0
roofs_gaps = 0
deleted_found = 0
white_panels_found = 0

DELETE_REFS = set([
    'R140219', 'R140246', 'R140273', 'R140300', 'R140326', 'R140365',
    'R140482', 'R140494', 'R140587', 'R140590', 'R140593', 'R140596', 'R140599'
])

found_vehiculos = False
found_camera = False
found_char_ctrl = False
found_cursor = False

buffering = False
depth = 0
buffer = []
current_ref = ""

with open(TARGET, "r", encoding="utf-8", errors="ignore") as fin:
    for line in fin:
        if '<Item ' in line:
            item_open += 1
        if '</Item>' in line:
            item_close += 1

        if 'Name="Vehiculos"' in line or '>Vehiculos<' in line:
            found_vehiculos = True
        if 'IsometricCamera' in line:
            found_camera = True
        if 'RBXSurvivorCharCtrl' in line:
            found_char_ctrl = True
        if 'RBXIsoCursorCtrl' in line:
            found_cursor = True

        if not buffering:
            if '<Item class="Part"' in line or '<Item class="WedgePart"' in line:
                m_ref = re.search(r'referent="([^"]+)"', line)
                current_ref = m_ref.group(1) if m_ref else ""
                buffering = True
                depth = 1
                buffer = [line]
                continue
        else:
            buffer.append(line)
            if '<Item ' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    buffering = False
                    if current_ref in DELETE_REFS:
                        deleted_found += 1

                    block = "".join(buffer)
                    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                    if m_name:
                        name = m_name.group(1)
                        name_lower = name.lower()

                        if name.startswith('Puerta_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                doors_false += 1
                        elif name.startswith('walls_exterior_') or name.startswith('walls_commercial_'):
                            if '<bool name="CanCollide">false</bool>' in block:
                                walls_false += 1
                            if '684037041b29ec20554a.png' in block:
                                white_panels_found += 1
                        elif 'roof' in name_lower or 'techo' in name_lower or 'ceiling' in name_lower:
                            if '<bool name="CanCollide">false</bool>' in block:
                                roofs_false += 1
                            m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
                            if m_sz:
                                sx, sz = float(m_sz.group(1)), float(m_sz.group(3))
                                if (2.85 < sx < 3.0) or (2.85 < sz < 3.0):
                                    roofs_gaps += 1

                    buffer = []

print("=== VERIFICATION REPORT ===")
print(f"Tag Balance: <Item> open = {item_open}, </Item> close = {item_close} -> MATCH = {item_open - item_close == 1}")
print(f"Doors with CanCollide=false: {doors_false} (expected 0)")
print(f"Walls with CanCollide=false: {walls_false} (expected 0)")
print(f"Roofs with CanCollide=false: {roofs_false} (expected 0)")
print(f"Roof gaps remaining [2.85 .. 3.00): {roofs_gaps} (expected 0)")
print(f"Obsolete House 33 parts found: {deleted_found} (expected 0)")
print(f"White panels remaining: {white_panels_found} (expected 0)")
print(f"Vehiculos intact: {found_vehiculos}")
print(f"Camera intact: {found_camera}")
print(f"Char Controller intact: {found_char_ctrl}")
print(f"Cursor intact: {found_cursor}")

if (item_open - item_close == 1 and doors_false == 0 and walls_false == 0 and
    roofs_false == 0 and roofs_gaps == 0 and deleted_found == 0 and
    white_panels_found == 0 and found_vehiculos and found_camera and
    found_char_ctrl and found_cursor):
    print("\nALL VERIFICATION CHECKS PASSED PERFECTLY!")
else:
    print("\nVERIFICATION FAILED!")
    sys.exit(1)

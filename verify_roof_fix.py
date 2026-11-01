import re
import sys

TARGET = r"out\PZ_Rosewood.rbxlx.tmp"

item_open = 0
item_close = 0
old_dark_texs_found = 0
right_slope_updated = 0
ridge_hidden_found = 0

found_vehiculos = False
found_camera = False
found_char_ctrl = False
found_cursor = False

buffering = False
depth = 0
buffer = []

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
            if '<Item class="Part"' in line:
                buffering = True
                depth = 1
                buffer = [line]
        else:
            buffer.append(line)
            if '<Item ' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    buffering = False
                    block = "".join(buffer)
                    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                    if m_name and m_name.group(1).startswith('roofs_30_06_'):
                        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?</CoordinateFrame>', block, re.DOTALL)
                        if m_cf:
                            m_z = re.search(r'<Z>([^<]+)</Z>', m_cf.group(0))
                            if m_z:
                                z = float(m_z.group(1))
                                if m_name.group(1) == 'roofs_30_06_100':
                                    if '<float name="Transparency">1</float>' in block:
                                        ridge_hidden_found += 1
                                elif z <= -43.0 and z >= -68.0:
                                    if any(old in block for old in ['d4d468f7657f6dd825aa.png', 'b73c2ccd6f14cf6b6e4f.png', '92cc8c628d8dc5bb8494.png']):
                                        old_dark_texs_found += 1
                                    if '4284505431' in block:
                                        right_slope_updated += 1
                    buffer = []

print("=== VERIFICATION REPORT ===")
print(f"Tag Balance Delta: {item_open - item_close} (expected 1)")
print(f"Right slope updated parts: {right_slope_updated} (expected 280)")
print(f"Old dark textures remaining on right slope: {old_dark_texs_found} (expected 0)")
print(f"Ridge billboard caps hidden: {ridge_hidden_found} (expected 35)")
print(f"Vehiculos intact: {found_vehiculos}")
print(f"Camera intact: {found_camera}")
print(f"Char Controller intact: {found_char_ctrl}")
print(f"Cursor intact: {found_cursor}")

if (item_open - item_close == 1 and right_slope_updated == 280 and
    old_dark_texs_found == 0 and ridge_hidden_found == 35 and
    found_vehiculos and found_camera and found_char_ctrl and found_cursor):
    print("\nALL VERIFICATION CHECKS PASSED PERFECTLY!")
else:
    print("\nVERIFICATION FAILED!")
    sys.exit(1)

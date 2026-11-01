import os

src = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

in_iso_camera = False
in_iso_source = False
source_lines_replaced = 0
found_cam = 0

with open(src, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'referent="R153412"' in line:
            in_iso_camera = True
            found_cam += 1
            print(f"Line {i}: Found R153412")
            continue
        if in_iso_camera:
            if '<ProtectedString name="Source"><![CDATA[' in line:
                in_iso_source = True
                print(f"Line {i}: Found Source CDATA start")
                continue
            if in_iso_source:
                source_lines_replaced += 1
                if ']]></ProtectedString>' in line:
                    in_iso_source = False
                    print(f"Line {i}: Found Source CDATA end, replaced {source_lines_replaced} lines")
                continue
            if '</Item>' in line:
                in_iso_camera = False
                print(f"Line {i}: End of R153412 item")
                break

print("Test scan completed. found_cam =", found_cam)

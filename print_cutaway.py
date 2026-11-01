import xml.etree.ElementTree as ET

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    collecting = False
    captured = []
    for line in f:
        if '<string name="Name">BuildingCutawayController</string>' in line:
            # We are inside BuildingCutawayController
            collecting = True
        if collecting:
            captured.append(line)
            if '</Item>' in line:
                break

xml_str = "<Item class='LocalScript'>\n" + "".join(captured)
root = ET.fromstring(xml_str)
src = root.find("./Properties/ProtectedString[@name='Source']")
if src is not None:
    print(src.text)
else:
    print("Source not found in captured XML")

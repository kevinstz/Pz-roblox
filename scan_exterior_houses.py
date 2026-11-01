import xml.etree.ElementTree as ET
import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Search in Exterior for any parts with walls_exterior_house or roofs_
house_parts = []
inside_exterior = False
stack = []

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)"', line)
        if m_item:
            stack.append({"class": m_item.group(1), "name": None})
            continue
        m_name = re.search(r'<string name="Name">(.*?)</string>', line)
        if m_name and stack:
            if stack[-1]["name"] is None:
                stack[-1]["name"] = m_name.group(1)
                if stack[-1]["name"] == "Exterior":
                    inside_exterior = True
                elif inside_exterior and len(stack) == 3: # direct child of Exterior (Exterior_XXXX_YYYY)
                    pass
        if inside_exterior:
            if any(k in line for k in ["walls_exterior_house", "walls_exterior_wooden", "roofs_"]):
                house_parts.append(line.strip())
        if '</Item>' in line:
            if stack:
                popped = stack.pop()
                if popped.get("name") == "Exterior":
                    inside_exterior = False
                    break

print(f"Total house/roof parts found in Exterior: {len(house_parts)}")
for p in house_parts[:20]:
    print(" ", p)

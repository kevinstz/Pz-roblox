import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

buildings = []
found_edificios = False
stack = [] # stack of item names or classes

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
                if stack[-1]["name"] == "Edificios":
                    found_edificios = True
                elif found_edificios and len(stack) >= 2 and stack[-2].get("name") == "Edificios":
                    buildings.append(stack[-1]["name"])
                    
        if '</Item>' in line:
            if stack:
                popped = stack.pop()
                if popped.get("name") == "Edificios":
                    found_edificios = False
                    break

print(f"Total Buildings directly under Edificios: {len(buildings)}")
for b in buildings:
    print(" -", b)

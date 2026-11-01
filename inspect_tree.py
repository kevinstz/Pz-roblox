import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Check what models exist in Workspace
models_summary = {}
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
                name = m_name.group(1)
                stack[-1]["name"] = name
                path = "/".join(s["name"] for s in stack if s.get("name"))
                if len(stack) <= 3:
                    print(f"Level {len(stack)}: {path}")
                    
        if '</Item>' in line:
            if stack:
                stack.pop()

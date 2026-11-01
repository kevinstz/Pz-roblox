import xml.etree.ElementTree as ET
import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Inspect parts named street_curbs or blends_ in Workspace
curb_parts = []
grass_overlay_parts = []

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    capturing = False
    lines = []
    for line in f:
        if '<Item class="Part"' in line:
            capturing = True
            lines = [line]
            continue
        if capturing:
            lines.append(line)
            if '</Item>' in line:
                capturing = False
                text = "".join(lines)
                if 'street_curbs' in text:
                    curb_parts.append(text)
                elif 'blends_grassoverlays' in text:
                    grass_overlay_parts.append(text)
                if len(curb_parts) >= 5 and len(grass_overlay_parts) >= 5:
                    break

print(f"Sample curb part:\n{curb_parts[0] if curb_parts else 'None'}")
print("=" * 60)
print(f"Sample grass overlay part:\n{grass_overlay_parts[0] if grass_overlay_parts else 'None'}")

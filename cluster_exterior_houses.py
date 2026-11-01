import xml.etree.ElementTree as ET
import re
from collections import defaultdict

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

clusters = defaultdict(list)
curr_ext = None

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<string name="Name">Exterior_' in line:
            m = re.search(r'<string name="Name">(Exterior_\d+_\d+)</string>', line)
            if m:
                curr_ext = m.group(1)
        if curr_ext and ('walls_exterior_house' in line or 'walls_exterior_wooden' in line):
            clusters[curr_ext].append(line.strip())

print("Clusters of exterior house walls in Exterior chunks:")
for ext_name, parts in sorted(clusters.items()):
    print(f"  {ext_name}: {len(parts)} exterior house wall parts")

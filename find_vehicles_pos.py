import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import xml.etree.ElementTree as ET
import os

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Find vehicle positions in PZ_Rosewood.rbxlx
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
matches = re.findall(r'<Item class="Model" referent="[^"]*">\s*<Properties>.*?<string name="Name">(Vehiculo_[^<]+)</string>.*?<CoordinateFrame name="CFrame">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text, re.DOTALL)
print(f"Found {len(matches)} vehicles:")
for name, x, y, z in matches:
    print(f"  {name}: pos=({float(x):.1f}, {float(y):.1f}, {float(z):.1f})")

import sys
import os

ROOT = r"C:\Users\julia\Downloads\pz_roblox_b42"
sys.path.insert(0, ROOT)
from pzlib.assets import PackIndex

packs = PackIndex(['Tiles2x.pack', 'Tiles2x.floor.pack'])

for i in [0, 1, 2, 8, 9, 10]:
    name = f"roofs_accents_01_{i}"
    spr = packs.sprite(name)
    if spr:
        spr.save(f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_{name}.png")
        print(f"Saved dbg_{name}.png, size={spr.size}")

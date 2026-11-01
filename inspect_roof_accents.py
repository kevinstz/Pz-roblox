import sys
import os

ROOT = r"C:\Users\julia\Downloads\pz_roblox_b42"
sys.path.insert(0, ROOT)
from pzlib.assets import PackIndex, load_all_tiles

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack'])
props = load_all_tiles()

print("Roofs accents:")
for i in range(16):
    name = f"roofs_accents_01_{i}"
    p = props.get(name, {})
    entry = packs.entries.get(name)
    print(f"  {name}: {p.get('TileType', '')} {p.get('GroupName', '')} entry={entry is not None}")

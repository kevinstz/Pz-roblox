import sys
import os

ROOT = r"C:\Users\julia\Downloads\pz_roblox_b42"
sys.path.insert(0, ROOT)
from pzlib.assets import PackIndex

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack'])

print("Searching for sprites...")
all_names = list(packs.entries.keys())
print(f"Total sprites in packs: {len(all_names)}")

roof_sprites = [n for n in all_names if "roof" in n.lower()]
siding_sprites = [n for n in all_names if "walls_exterior_house" in n.lower() or "walls_exterior_wooden" in n.lower()]
carpentry_sprites = [n for n in all_names if "carpentry" in n.lower() or "fencing" in n.lower()]
fixtures_ac = [n for n in all_names if "aircond" in n.lower() or "vent" in n.lower() or "appliances" in n.lower()]
antennas = [n for n in all_names if "antenna" in n.lower() or "roofs_acc" in n.lower()]

print(f"Roof sprites ({len(roof_sprites)}):", roof_sprites[:15])
print(f"Siding sprites ({len(siding_sprites)}):", siding_sprites[:15])
print(f"Carpentry sprites ({len(carpentry_sprites)}):", carpentry_sprites[:15])
print(f"AC / vent sprites ({len(fixtures_ac)}):", fixtures_ac[:15])
print(f"Antenna sprites ({len(antennas)}):", antennas[:15])

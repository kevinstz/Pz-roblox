import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, load_all_tiles
from pzlib.geometry import load_tile_geometry

props = load_all_tiles()
geom = load_tile_geometry()

print("Curb props:")
for i in [0, 1, 4, 10, 11]:
    n = f'street_curbs_01_{i}'
    print(n, "props:", props.get(n), "geom:", geom.get(n))

n_grass = 'blends_grassoverlays_01_0'
print(n_grass, "props:", props.get(n_grass), "geom:", geom.get(n_grass))

for n in ['blends_natural_01_0', 'blends_natural_01_64', 'blends_street_01_48']:
    print(n, "props:", props.get(n))


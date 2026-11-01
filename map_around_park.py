import sys, os
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA

squares, rooms, headers = load_region(os.path.join(MEDIA, 'maps', 'Muldraugh, KY'), 8040, 11585, 8165, 11760)

# Park billboard is at x=8087, y=11667..11672
# In Roblox coordinates:
# OX = 8102.5, OY = 11672.5
# x = 8087 -> cx = (8087 - 8102.5)*3 = -46.5
# y = 11670 -> cz = (11670 - 11672.5)*3 = -7.5
# Look at the squares around x: 8080..8105, y: 11650..11675
for y in range(11655, 11675):
    line = f"y={y}: "
    for x in range(8085, 8095):
        sq = squares.get((x, y, 0), [])
        b0 = sq[0] if sq else "EMPTY"
        if "street" in b0:
            c = "S"
        elif "natural" in b0:
            c = "G"
        elif "tiles" in b0:
            c = "T"
        else:
            c = "?"
        line += c
    print(line)

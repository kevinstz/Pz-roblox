# In dense_10_2.83s.jpg:
# The bee avatar is at (x=964, y=661)
# The park is to the upper left.
# Park coordinates in PZ Rosewood:
# Park center is approx PZ x=8087, y=11669
# In Roblox world:
# cx = (8087 - 8102.5) * 3 = -46.5
# cz = (11669 - 11672.5) * 3 = -10.5
# The street crossing is at PZ x=8096, y=11669 -> Roblox cx = -19.5, cz = -10.5
# The parking lot where player is standing:
# Where is that parking lot?
# Let's check parking lot coordinates in PZ!
import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA

MAPDIR = rf"{MEDIA}\maps\Muldraugh, KY"
# Let's search where police cars or parking stalls are:
# In previous turn, police station parking lot was at:
# x around 8090..8110, y around 11700..11730
print("PZ world coords for police parking:")
print("x=8100 -> cx =", (8100 - 8102.5) * 3.0)
print("y=11710 -> cz =", (11710 - 11672.5) * 3.0)

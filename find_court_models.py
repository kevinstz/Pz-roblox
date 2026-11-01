# Find buildings with parts in X in [-30, 40], Z in [-60, 20]
from dump_pair2_region import dump_pair2_region
found = dump_pair2_region()

blds = set()
for p in found:
    if -30 <= p[2] <= 40 and -60 <= p[4] <= 20 and p[3] > 1.0:
        blds.add(" -> ".join(p[5]))

print("Models in that area:")
for b in sorted(blds):
    print(" ", b)

# Cars are at X = -21, Z in [-60, -36]
# Let us find parts within 50 studs of (-21, -60) in all directions:
from dump_pair2_region import dump_pair2_region
found = dump_pair2_region()

nearby = [p for p in found if -40 <= p[2] <= 10 and -90 <= p[4] <= -10]
print(f"Total parts near cars: {len(nearby)}")
# Group by parent
by_parent = {}
for p in nearby:
    par = " -> ".join(p[5])
    by_parent[par] = by_parent.get(par, 0) + 1
for k, v in sorted(by_parent.items()):
    print(f"  {k}: {v}")

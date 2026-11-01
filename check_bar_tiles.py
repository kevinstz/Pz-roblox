# Let us inspect the actual PZ tile names in Bar_31_45_12
from dump_pair2_region import dump_pair2_region

found = dump_pair2_region()

bar_parts = [p for p in found if 'Bar_31_45_12' in p[5] and 'Piso_0' in p[5]]
print(f"Total parts in Bar_31_45_12 Piso_0: {len(bar_parts)}")
# Look at exterior walls of Bar_31_45_12
for p in bar_parts:
    if 'wall' in p[0].lower() and -55 <= p[2] <= -45 and -75 <= p[4] <= -55:
        print(f"Ref={p[7]} | Name={p[0]:30s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f})")

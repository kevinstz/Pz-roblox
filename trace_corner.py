# Let us trace character position by looking at camera focus / rootPart or tracking world coordinates
# Let us calculate the world coordinate of the corner of Bar_31_45_12:
from dump_pair2_region import dump_pair2_region
found = dump_pair2_region()

corner_parts = [p for p in found if -50 <= p[2] <= -44 and -75 <= p[4] <= -50]
print(f"Total parts in corner: {len(corner_parts)}")
for p in sorted(corner_parts, key=lambda x: (x[4], x[3])):
    print(f"{p[7]} | {p[0]} | Class={p[1]} | pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | parent={p[5]}")

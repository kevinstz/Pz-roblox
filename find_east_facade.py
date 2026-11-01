from dump_pair2_region import dump_pair2_region
found = dump_pair2_region()

print("Parts with X > -47 and Z between -70 and -50:")
for p in found:
    if -47 <= p[2] <= -35 and -70 <= p[4] <= -50:
        print(f"Ref={p[7]} | Name={p[0]} | Class={p[1]} | pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Parent={p[5]}")

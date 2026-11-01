from dump_pair2_region import dump_pair2_region

found = dump_pair2_region()

print("Parts with Z between -68.0 and -66.5:")
for p in found:
    if -68.0 <= p[4] <= -66.5:
        print(f"Ref={p[7]} | Name={p[0]:30s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f}) | Parent={p[5]}")

from dump_pair2_region import dump_pair2_region
found = dump_pair2_region()

for p in found:
    name = p[0].lower()
    if 'fixtures_windows' in name or 'commercial_01_58' in name or 'glass' in name:
        if -60 <= p[2] <= -40 and -75 <= p[4] <= -55:
            print(f"Ref={p[7]} | Name={p[0]} | Pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Parent={p[5]}")

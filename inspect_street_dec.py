from dump_pair2_region import dump_pair2_region
found = dump_pair2_region()

for p in found:
    if p[7] in ['R133864', 'R133583', 'R133584', 'R133585']:
        print("=== PART", p[7], p[0], "pos=", (p[2], p[3], p[4]), "===")
        print(p[6][:500])

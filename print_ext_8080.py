from dump_pair2_region import dump_pair2_region

found = dump_pair2_region()

ext_8080 = [p for p in found if 'Exterior_8080_11648' in p[5]]
print(f"Total in Exterior_8080_11648: {len(ext_8080)}")

types = {}
for p in ext_8080:
    t = p[0].split('_')[0]
    types[t] = types.get(t, 0) + 1
print("Types in Exterior_8080_11648:", types)

for p in ext_8080:
    pname = p[0].lower()
    if any(k in pname for k in ['wall', 'roof', 'window', 'door', 'wedge', 'cornice', 'trim', 'deck', 'shallow', 'accent']):
        print(f"Ref={p[7]}, Name={p[0]}, Class={p[1]}, pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f})")

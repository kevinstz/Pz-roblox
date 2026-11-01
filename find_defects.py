from dump_pair2_region import dump_pair2_region

found = dump_pair2_region()

print("=== DEFECT 1: Floating White Door / Arch at Lower-Left Building ===")
# Lower-left building is Bar_31_45_12 / Exterior_8080_11648.
# Facade facing the parking lot is around X in [-55, -45], Z in [-75, -55].
# Let's inspect parts near X in [-50, -44], Z in [-65, -58], Y in [0, 8]:
for p in found:
    if -50 <= p[2] <= -44 and -66 <= p[4] <= -57 and 0 <= p[3] <= 9:
        print(f"Defect 1 cand: {p[7]} | {p[0]} | Class={p[1]} | pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Parent={p[5]}")

print("\n=== DEFECT 2: Parapet Pale Panels (Bar_31_45_12 / Exterior_8080_11648) ===")
# The parapet wall runs along the edge of the roof.
# In v4_f6_center.jpg, the parapet has brown brick, but several parts are pale cyan/white.
# The parapet top is around Y in [6, 11], along X in [-55, -45], Z in [-75, -55].
for p in found:
    if -55 <= p[2] <= -44 and -75 <= p[4] <= -55 and 5 <= p[3] <= 12:
        # Check part name or decals inside lines:
        lines = p[6]
        # Check if it has decals or textures or Color3:
        print(f"Parapet cand: {p[7]} | {p[0]} | pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Parent={p[5]}")

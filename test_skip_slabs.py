import xml.etree.ElementTree as ET

# Test identifying the 4 ceiling slabs
target_positions = [
    (157.5, 7.3, 19.5),
    (153.0, 7.3, 33.0),
    (183.0, 7.3, -235.5),
    (186.0, 7.3, -222.0)
]

def matches_target(x, y, z):
    for tx, ty, tz in target_positions:
        if abs(x - tx) < 0.5 and abs(y - ty) < 0.5 and abs(z - tz) < 0.5:
            return True
    return False

print("Checker ready.")

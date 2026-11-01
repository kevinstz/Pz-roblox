import numpy as np

# Test geometry bounds for House 28:
# Footprint: X in [178.5 .. 187.5], Z in [-247.5 .. -220.5]
# Ridge at X = 183.0. Y_eaves = 7.35, H = 2.25 -> Y_ridge = 9.60.
# Overhang = 0.6 studs.
# West slope covers X from 177.9 to 183.0 (width = 5.1). Center X = 180.45.
# East slope covers X from 183.0 to 188.1 (width = 5.1). Center X = 185.55.
# Length = 27.0 + 1.0 overhang = 28.0 (Z from -248.0 to -220.0). Center Z = -234.0.
# Center Y = 7.35 + 2.25/2 = 8.475.

print("House 28 Roof:")
print("  West slope pos:", (180.45, 8.475, -234.0), "size:", (28.0, 2.25, 5.1))
print("  East slope pos:", (185.55, 8.475, -234.0), "size:", (28.0, 2.25, 5.1))
print("  Gable North West half pos:", (180.75, 8.475, -247.45), "size:", (0.2, 2.25, 4.5))
print("  Gable North East half pos:", (185.25, 8.475, -247.45), "size:", (0.2, 2.25, 4.5))

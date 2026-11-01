# Roblox WedgePart standard geometry:
# In local space of WedgePart (CFrame = Identity):
# Size = (X, Y, Z) = (sx, sy, sz)
# - Bottom face is at Y = -sy/2 (normal = (0, -1, 0))
# - Back vertical face is at Z = +sz/2 (normal = (0, 0, 1))
# - Slope connects top back edge (Y = +sy/2, Z = +sz/2) to bottom front edge (Y = -sy/2, Z = -sz/2)
# - Normal of slope has +Y and -Z components!
# Therefore:
# If we want a roof slope that slopes downward in the +X direction (falling towards +X):
# We rotate the wedge by 90 degrees around Y axis (or -90 degrees)!
# Let's verify rotation matrices:
import numpy as np

def rot_y_deg(deg):
    r = np.radians(deg)
    c, s = np.cos(r), np.sin(r)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

# Standard wedge: slope falls towards -Z (local forward)
# If rotated by Y = -90 deg:
# local -Z becomes world +X!
# So slope falls towards world +X!
R_fall_plus_x = rot_y_deg(-90)
print("Rotation for slope falling to +X (rot_y -90):")
print(R_fall_plus_x)
# In this orientation, local X is world +Z, local Z is world -X.
# Size of wedge must be: (Z_length, Height, X_slope_span) = (L, H, W)

# If rotated by Y = +90 deg:
# local -Z becomes world -X!
# So slope falls towards world -X!
R_fall_minus_x = rot_y_deg(90)
print("Rotation for slope falling to -X (rot_y +90):")
print(R_fall_minus_x)

import numpy as np

# Blue car is at X_b, Z_b. Black car is at X_k, Z_k.
# In screen space:
# RightVector = (0.707, 0, -0.707).
# d = pt - cam_pos = pt - (focus - look * 115)
# x_cam = dot(pt - focus, right)
# u = (x_cam / (115 * tan(13.5/2) * (1920/1080))) * 960 + 960

# Screen width factor:
factor_u = 960.0 / (115.0 * np.tan(np.radians(13.5 / 2.0)) * (16.0 / 9.0))
# Screen height factor:
factor_v = 540.0 / (115.0 * np.tan(np.radians(13.5 / 2.0)))

print(f"factor_u = {factor_u:.3f} px/stud, factor_v = {factor_v:.3f} px/stud")

# Let's test which pair of cars has delta_u = 1350 - 1050 = 300 px:
cars = [
    ("Pair 1", (-78.0, -138.0), (-57.0, -138.0)),
    ("Pair 2", (-21.0, -60.0), (-21.0, -36.0)),
    ("Pair 3", (69.0, -66.0), (90.0, -66.0)),
    ("Pair 4", (153.0, -150.0), (153.0, -120.0)),
]

for name, (x1, z1), (x2, z2) in cars:
    dx = x2 - x1
    dz = z2 - z1
    # dot with right: (dx - dz) * 0.7071
    du = (dx - dz) * np.sqrt(0.5) * factor_u
    # dot with up: (-0.3535*dx - 0.3535*dz)
    dv = - (-0.3535 * dx - 0.3535 * dz) * factor_v
    print(f"{name}: du = {du:.1f} px, dv = {dv:.1f} px")
